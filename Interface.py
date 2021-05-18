# coding=utf-8
# import ConfigParser
import ReadConfig
import os
import re
import struct
import pymysql
import time
from flask import Flask, request, render_template, make_response
from werkzeug.utils import secure_filename
import json
from predict import Seg
from procdata import classify, PictureLocation
from fire_boundary import FireArea, FireBoundary, pointsample
from OnWriteHandler import *
import os,datetime
from operator import itemgetter
from FireClassification.classification import FireClassification
from trendpredict import centerobj


app = Flask(__name__)

# 读取数据库配置文件
db = ReadConfig.getSQLCONFIG(r'./db.ini')

# 设置数据库连接参数
app.config['DATABASE'] = db[0]
app.config['HOST'] = db[1]
app.config['USERNAME'] = db[2]
app.config['PWD'] = db[3]
app.config['backwardAngle'] = db[4]
app.config['sideAngle'] = db[5]

# 接收图像以及图像信息数据
@app.route('/putData', methods=['POST'])
def putData():
    # 执行返回值
    result = {'code': 200, 'msg': "success", 'data': None}
    flag =0
    i = 1
    if request.method == 'POST':
        # 获取图片
        # img = request.files['img']
        # 获取图片key值
        imgkey = request.form.get('key')
        # 获取图片信息数据
        imgData = json.loads(request.form.get('imgData'))
        # 连接数据库
        db = pymysql.connect(host=app.config['HOST'], user=app.config['USERNAME'], password=app.config['PWD'],
                             database=app.config['DATABASE'])
        # 使用 cursor() 方法创建一个游标对象 cursor
        cur = db.cursor()
        # 接收到的图片保存到本地
        if not os.path.exists("./tempImages/"):
            os.mkdir("./tempImages/")
        path = "./tempImages/"
        File_all = os.listdir(path)
        # 获取当前文件路径
        File_new = os.path.abspath(path)
        # print(File_new)
        # File_new[:-8]截去当前文件名，获得文件夹路径
        # 通过os.path.join将文件路径与文件名进行拼接并存为列表
        li_name = [os.path.join(File_new, i) for i in File_all]
        # 通过os.path.getmtime获取所有所有文件创建的时间戳并存为列表
        li_time = [os.path.getmtime(j) for j in li_name]
        # 定义函数
        def combination(i, j):
            di = {'fileName': i, 'createTime': j}
            return di
        # 列表推导式用来转化为itemgetter方法的格式要求
        li_item = [combination(i, j) for i, j in zip(File_all, li_time)]
        # 按创建时间开始排序
        top = sorted(li_item, key=itemgetter('createTime'), reverse=True)
        # 获取新增图片路径
        imgpath=os.path.join("./tempImages",top[0]['fileName'])
        pictureLocation = PictureLocation(imgData["flyAngle"], imgData["longitude"], imgData["latitude"], imgData["height"],
                                    app.config['sideAngle'], app.config['backwardAngle'],imgData["planePitchAngle"],imgData["cameraPitchAngle"], imgData["cameraAngle"])
        if pictureLocation != None:
            # 图像中心经纬度
            centerLongitude = pictureLocation[0][0]
            centerLatitude = pictureLocation[0][1]
            # 图片四周经纬度
            strpictureLocation = str(pictureLocation[1][0])+','+str(pictureLocation[1][1])+','+str(pictureLocation[2][0])+','+str(pictureLocation[2][1])+','+str(pictureLocation[3][0])+','+str(pictureLocation[3][1])+','+str(pictureLocation[4][0])+','+str(pictureLocation[4][1])
            # print(strpictureLocation)
            # 执行sql语句，将图片信息入库
            sql = "INSERT INTO video_coordinate (task_id,codes,margin_point,create_date) VALUES ('" + imgData[
                "task_id"] + "','" + imgkey + "','" + strpictureLocation + "','" + imgData["create_date"] + "')"
            try:
                # 执行sql语句
                cur.execute(sql)
                # 提交到数据库执行
                db.commit()
                print('margin_point saved!')

            except Exception as e:
                print("There are mistakes:", e)
                # 如果发生错误则回滚
                db.rollback()

                result["code"] = -1
                result["msg"] = "failed"
                result["key"] = imgkey
            # 图片分类是否存在火灾
            # 若存在火灾，对图片进行语义分割
            if (FireClassification(imgpath)=="fire"):
                img_id = 1
                result_path = Seg(imgpath, "./checkpoints/2020-12-02_19_42_08/model_epoch_50")
                # 火际线经纬度
                fire_boundary = FireBoundary(result_path, pictureLocation, imgData["flyAngle"], imgData["height"],
                                             app.config['sideAngle'],
                                             app.config['backwardAngle'], imgData["cameraAngle"],
                                             imgData["planePitchAngle"], imgData["cameraPitchAngle"])
                # 图片内火区个数
                area_num = len(fire_boundary)
                for i in range(0, area_num):
                    fire_boundarys = []
                    f = pointsample(fire_boundary[i])
                    for k in range(0, len(f)):
                        fire_boundarys.append(f[k][0])
                        fire_boundarys.append(f[k][1])
                    fire_information = "fire"
                    sql1 = "INSERT INTO fire_situation (img_id,task_id,fire_info,location,create_date) VALUES ("+str(img_id)+","+imgData["task_id"]+",'"+ fire_information +"','"+ str(fire_boundarys) +"','" + imgData["create_date"] + "')"
                    predict_boundary = centerobj(f)
                    predict_minutes = 15
                    sql2 = "INSERT INTO fire_predict_situation(img_id,task_id,fire_info,location,predict_minutes,create_date) VALUES ("+str(img_id)+","+imgData["task_id"]+",'"+ fire_information +"','"+ str(predict_boundary) +"',"+ str(predict_minutes) +",'" + imgData["create_date"] + "')"
                    try:
                        cur.execute(sql1)
                        cur.execute(sql2)
                        db.commit()
                        print('fire_info saved')

                    except Exception as e:
                        print("There are mistakes:", e)
                        # 如果发生错误则回滚
                        db.rollback()
                        result["code"] = -1
                        result["msg"] = "failed"
                        result["key"] = imgkey
                db.close()
                img_id += 1
                result["key"] = imgkey
                return result
            # 关闭数据库连接
            db.close()
            result["key"] = imgkey
            return result


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
