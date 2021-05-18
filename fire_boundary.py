import cv2
import numpy as np
import math
from PIL import Image
import matplotlib.pyplot as plt


# 获取轮廓边界像素点位置
def GetContours(filePath):
    img = cv2.imread(filePath)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray, 0, 128, cv2.THRESH_BINARY)
    realContours = []
    image, contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    max_contour = max(contours, key=len)
    realContours.append(max_contour)
    for contour in contours:
        for pixel in contour[0]:
            x = pixel[0]
            y = pixel[1]
        tempDist = -1
        for realContour in realContours:
            dist2 = cv2.pointPolygonTest(realContour, (x, y), False)
            if dist2 >= 0:
                tempDist = 1
        if tempDist < 0 and len(contour) > 30:
            realContours.append(contour)
    # cv2.drawContours(img, realContours, -1, (255, 255, 255), 3)
    # plt.imshow(img)
    # plt.axis('on')
    # plt.title('image')
    # plt.show()
    return realContours, img.shape[0], img.shape[1]

# 处理传入的参数，得到拍摄图片实际的长宽还有飞行夹角
def BasicInformation(flyAngle, height, sideAngle, backwardAngle, cameraAngle, planePitchAngle, cameraPitchAngle):
    flyAngle = float(flyAngle)
    height = float(height)
    sideAngle = float(sideAngle)
    backwardAngle = float(backwardAngle)
    cameraAngle = float(cameraAngle)
    planePitchAngle = float(planePitchAngle)
    cameraPitchAngle = float(cameraPitchAngle)
    height = height / 1000
    # 将飞机航向负角度转换为相应的正角度
    if flyAngle < 0:
        flyAngle = 360 + flyAngle
        # 计算中心点经纬度
    angle_diff = 90 - planePitchAngle + cameraPitchAngle
    # 判断摄像头所拍图片是否合格
    if angle_diff >= 90 or cameraPitchAngle > 0:
        return None
    dcf_diff = height * math.tan(math.radians(angle_diff))
    # 角度转换为弧度
    sideAngle = math.radians(sideAngle)
    length = height * math.tan(sideAngle)
    width = dcf_diff - height * math.tan(math.radians(angle_diff - backwardAngle))
    flyAngle = 180 + flyAngle + cameraAngle
    return length, width, flyAngle

# 计算每个像素点的经纬度
def PixelLocation(pixel, picturelocation, picWidth, picLength, flyAngle, height, sideAngle,
                  backwardAngle, cameraAngle, planePitchAngle, cameraPitchAngle):
    # 计算边际点最大纬度和最低经度
    max_latitude = np.max(picturelocation, axis=0)[1]
    min_longitude = np.min(picturelocation, axis=0)[0]
    pic_real_length, pic_real_width, flyAngle = BasicInformation(flyAngle, height, sideAngle, backwardAngle, cameraAngle, planePitchAngle, cameraPitchAngle)
    # 获取每个像素点占据的长度和宽度
    pixel_width = 2 * pic_real_width / picWidth
    pixel_length = 2 * pic_real_length / picLength
    # 计算像素点距离最高纬度的纵向距离
    diff_width = pixel[0] * pixel_width * abs(math.cos(math.radians(flyAngle))) \
                 + (2 * pic_real_length - pixel[1] * pixel_length) * abs(math.sin(math.radians(flyAngle)))
    pixel_latitude = max_latitude - diff_width / 111
    # 计算像素点与最低经度之间的横向距离
    diff_length = pixel[0] * pixel_width * abs(math.sin(math.radians(flyAngle))) + pixel[1] * pixel_length * abs(math.cos(math.radians(flyAngle)))
    pixel_longitude = min_longitude + diff_length / 111 * math.cos(math.radians(pixel_latitude))
    return pixel_longitude, pixel_latitude


# 计算整个火际线像素点的经纬度
def FireBoundary(filepath, picturelocation, flyAngle, height, sideAngle,
                  backwardAngle, cameraAngle, planePitchAngle, cameraPitchAngle):
    boundaries, picWidth, picLength = GetContours(filepath)
    fire_boundary = []
    fire_boundaries = []
    for boundary in boundaries:
        for pixel in boundary:
            pixel_longitude_value, pixel_latitude_value = PixelLocation(pixel[0], picturelocation, picWidth, picLength, flyAngle, height, sideAngle,
                                backwardAngle, cameraAngle, planePitchAngle, cameraPitchAngle)
            fire_boundary.append([pixel_longitude_value,pixel_latitude_value])
            # fire_boundary.append(pixel_latitude_value)
        fire_boundaries.append(fire_boundary)
        fire_boundary = []
    return fire_boundaries


# 计算火情面积
def FireArea(filepath, flyAngle, height, sideAngle, backwardAngle, cameraAngle, planePitchAngle, cameraPitchAngle):
    img = Image.open(filepath)
    fire_num = 0
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            px = img.getpixel((x, y))
            if px[1] == 255:
                fire_num = fire_num + 1
    img_area = img.size[0] * img.size[1]
    length, width, flyAngle = BasicInformation(flyAngle, height, sideAngle, backwardAngle,
                                                                  cameraAngle, planePitchAngle, cameraPitchAngle)
    fire_areas = (fire_num / img_area) * length * width
    print(fire_num, img_area, length, width)
    return fire_areas

# 选出边缘四点作为轮廓点
def pointsample(f):
    length = len(f)
    f_pointsample = []
    maxlongflag = 0
    maxlatiflag = 0
    minlongflag = 0
    minlatiflag = 0
    maxlong = f[0][0]
    maxlati = f[0][1]
    minlong = f[0][0]
    minlati = f[0][1]
    for i in range(1, length):
        if f[i][0] > maxlong:
            maxlongflag = i
            maxlong = f[i][0]
        if f[i][1] > maxlati:
            maxlatiflag = i
            maxlati = f[i][1]
        if f[i][0] < minlong:
            minlongflag = i
            minlong = f[i][0]
        if f[i][1] < minlati:
            minlatiflag = i
            minlati = f[i][1]

    f_pointsample.append(f[minlongflag])
    f_pointsample.append(f[maxlatiflag])
    f_pointsample.append(f[maxlongflag])
    f_pointsample.append(f[minlatiflag])
    return f_pointsample




if __name__ == '__main__':
    pic_path = "preds//68.jpg"
    fire_boundary = FireBoundary(pic_path, [[35, 36]], 60, 111, 30, 60, 15, 15, -19)
    # print(fire_boundary)
    # print(len(fire_boundary))
    for i in fire_boundary:
        # print(i)
        print(pointsample(i))
        # print(len(i))
    # fire_area = FireArea(pic_path, 60, 111, 30, 60, 15, 15, -19)
    # fire_boundary_x = []
    # fire_boundary_y = []
    # for i in fire_boundary[7]:
    #     fire_boundary_x.append(i[0])
    #     fire_boundary_y.append(i[1])
    # plt.scatter(fire_boundary_x, fire_boundary_y, color='g', label='fire', linewidth=0.1)
    # plt.show()
    # print('fire', fire_boundary, len(fire_boundary))
    # print(fire_area)
    # GetContours(pic_path)


