# -*- coding: utf-8 -*-
# @Time    : 2017/12/8
# @Author  : fc.w
# @File    : center_point_of_coordinates.py
from math import cos, sin, atan2, sqrt, radians, degrees
import math
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
import sklearn
from fire_boundary import pointsample

class CenterPointFromListOfCoordinates:
    def center_geolocation(self, geolocations):
        """
        输入多个经纬度坐标，找出中心点
        :param geolocations: 集合
        :return:
        """
        x = 0
        y = 0
        z = 0
        length = len(geolocations)
        for lon, lat in geolocations:
            lon = radians(float(lon))
            lat = radians(float(lat))
            x += cos(lat) * cos(lon)
            y += cos(lat) * sin(lon)
            z += sin(lat)

        x = float(x / length)
        y = float(y / length)
        z = float(z / length)

        return (degrees(atan2(y, x)), degrees(atan2(z, sqrt(x * x + y * y))))


def millerToXY(lon, lat):
    """
    :param lon: 经度
    :param lat: 维度
    :return:
    """

    L = 6381372 * math.pi * 2  # 地球周长
    W = L  # 平面展开，将周长视为X轴
    H = L / 2  # Y轴约等于周长一般
    mill = 2.3  # 米勒投影中的一个常数，范围大约在正负2.3之间
    x = lon * math.pi / 180  # 将经度从度数转换为弧度
    y = lat * math.pi / 180
    # 将纬度从度数转换为弧度
    y = 1.25 * math.log(math.tan(0.25 * math.pi + 0.4 * y))  # 这里是米勒投影的转换

    # 这里将弧度转为实际距离 ，转换结果的单位是公里
    x = (W / 2) + (W / (2 * math.pi)) * x
    y = (H / 2) - (H / (2 * mill)) * y
    xy_coordinate = [int(round(x)), int(round(y))]
    return xy_coordinate


def millerToLonLat(x,y):
    """
    将平面坐标系中的x,y转换为经纬度，利用米勒坐标系
    :param x: x轴
    :param y: y轴
    :return:
    """
    # lonlat_coordinate = []
    L = 6381372 * math.pi*2
    W = L
    H = L/2
    mill = 2.3
    lat = ((H/2-y)*2*mill)/(1.25*H)
    lat = ((math.atan(math.exp(lat))-0.25*math.pi)*180)/(0.4*math.pi)
    lon = (x-W/2)*360/W
    lonlat_coordinate = [round(lon,7),round(lat,7)]
    return lonlat_coordinate


def centerobj(f):
    centerObj = CenterPointFromListOfCoordinates()
    centre_point = centerObj.center_geolocation(f)
    # print('The centre point is: ', centre_point)
    centre_point_coordinate = millerToXY(centre_point[0], centre_point[1])
    # print('The centre point coordinate is: ', centre_point_coordinate)

    f_coordinate = []
    f_coordinate_x = []
    f_coordinate_y = []
    for i in range(len(f)):
        f_coordinate.append(millerToXY(f[i][0], f[i][1]))
    # print("The origin is: ", f_coordinate)
    for index in range(len(f_coordinate)):
        f_coordinate_x.append(f_coordinate[index][0])
        f_coordinate_y.append(f_coordinate[index][1])

    f_coordinate_2min = []
    f_coordinate_2min_x = []
    f_coordinate_2min_y = []
    for j in range(len(f)):
        point = millerToXY(f[j][0], f[j][1])
        point[0] = point[0] + 60 / 1000 * (point[0] - centre_point_coordinate[0]) / pow(
            pow((point[0] - centre_point_coordinate[0]), 2) +
            pow((point[1] - centre_point_coordinate[1]), 2), 0.5)
        point[1] = point[1] + 60 / 1000 * (point[1] - centre_point_coordinate[1]) / pow(
            pow((point[0] - centre_point_coordinate[0]), 2) +
            pow((point[1] - centre_point_coordinate[1]), 2), 0.5)

        f_coordinate_2min.append(point)
    for index in range(len(f_coordinate_2min)):
        f_coordinate_2min_x.append(f_coordinate_2min[index][0])
        f_coordinate_2min_y.append(f_coordinate_2min[index][1])

    f_coordinate_5min = []
    f_coordinate_5min_x = []
    f_coordinate_5min_y = []
    for j in range(len(f)):
        point = millerToXY(f[j][0], f[j][1])
        point[0] = point[0] + 300 / 1000 * (point[0] - centre_point_coordinate[0]) / pow(
            pow((point[0] - centre_point_coordinate[0]), 2) +
            pow((point[1] - centre_point_coordinate[1]), 2), 0.5)
        point[1] = point[1] + 300 / 1000 * (point[1] - centre_point_coordinate[1]) / pow(
            pow((point[0] - centre_point_coordinate[0]), 2) +
            pow((point[1] - centre_point_coordinate[1]), 2), 0.5)

        f_coordinate_5min.append(point)
    # print(f_coordinate_5min)
    for index in range(len(f_coordinate_5min)):
        f_coordinate_5min_x.append(f_coordinate_5min[index][0])
        f_coordinate_5min_y.append(f_coordinate_5min[index][1])

    f_coordinate_10min = []
    f_coordinate_10min_x = []
    f_coordinate_10min_y = []
    for j in range(len(f)):
        point = millerToXY(f[j][0], f[j][1])
        point[0] = point[0] + 800 / 1000 * (point[0] - centre_point_coordinate[0]) / pow(
            pow((point[0] - centre_point_coordinate[0]), 2) +
            pow((point[1] - centre_point_coordinate[1]), 2), 0.5)
        point[1] = point[1] + 800 / 1000 * (point[1] - centre_point_coordinate[1]) / pow(
            pow((point[0] - centre_point_coordinate[0]), 2) +
            pow((point[1] - centre_point_coordinate[1]), 2), 0.5)

        f_coordinate_10min.append(point)
    # print(f_coordinate_10min)
    for index in range(len(f_coordinate_10min)):
        f_coordinate_10min_x.append(f_coordinate_10min[index][0])
        f_coordinate_10min_y.append(f_coordinate_10min[index][1])

    # plt.scatter(f_coordinate_2min_x,f_coordinate_2min_y, color='b',label='fire',linewidth =0.5)
    # plt.scatter(f_coordinate_5min_x,f_coordinate_5min_y,color='r',label='fire',linewidth =0.5)
    # plt.scatter(f_coordinate_10min_x,f_coordinate_10min_y,color='y',label='fire',linewidth =0.5)
    # plt.show()

    y_train = [f_coordinate_x, f_coordinate_2min_x, f_coordinate_5min_x, f_coordinate_10min_x]
    x_train = [0, 2, 5, 10]
    x_test = [15, 20, 30]
    x_train = np.array(x_train).reshape(-1, 1)
    x_test = np.array(x_test).reshape(-1, 1)
    model = LinearRegression()
    model.fit(x_train, y_train)
    y_pre = model.predict(x_test)

    y_train_1 = [f_coordinate_y, f_coordinate_2min_y, f_coordinate_5min_y, f_coordinate_10min_y]
    x_train_1 = [0, 2, 5, 10]
    x_test_1 = [15, 20, 30]
    x_train_1 = np.array(x_train_1).reshape(-1, 1)
    x_test_1 = np.array(x_test_1).reshape(-1, 1)
    model1 = LinearRegression()
    model1.fit(x_train_1, y_train_1)
    y_pre_1 = model1.predict(x_test_1)

    # plt.scatter(f_coordinate_2min_x, f_coordinate_2min_y, color='g', label='fire', linewidth=0.5)
    # plt.scatter(f_coordinate_5min_x,f_coordinate_5min_y,color='r',label='fire',linewidth =0.5)
    # plt.scatter(f_coordinate_10min_x,f_coordinate_10min_y,color='y',label='fire',linewidth =0.5)
    # plt.scatter(y_pre[0], y_pre_1[0], color='b', label='fire', linewidth=0.5)
    # plt.scatter(y_pre[1], y_pre_1[1],color='r',label='fire',linewidth =0.5)
    # plt.scatter(y_pre[2], y_pre_1[2],color='y',label='fire',linewidth =0.5)
    # plt.show()
    F_coordinate_15min = []
    f_coordinate_15min = []
    f_coordinate_20min = []
    f_coordinate_30min = []
    for index in range(len(y_pre[0])):
        f_coordinate_15min.append(millerToLonLat(y_pre[0][index], y_pre_1[0][index]))
    f_coordinate_15min = pointsample(f_coordinate_15min)
    length = len(f_coordinate_15min)
    for i in range(0, length):
        F_coordinate_15min.append(f_coordinate_15min[i][0])
        F_coordinate_15min.append(f_coordinate_15min[i][1])
    # print("15 min is:", f_coordinate_15min)

    for index in range(len(y_pre[1])):
        f_coordinate_20min.append(millerToLonLat(y_pre[1][index], y_pre_1[1][index]))
    # print("20 min is:", f_coordinate_20min)

    for index in range(len(y_pre[2])):
        f_coordinate_30min.append(millerToLonLat(y_pre[2][index], y_pre_1[2][index]))
    # print("30 min is:", f_coordinate_30min)
    return F_coordinate_15min, f_coordinate_20min, f_coordinate_30min

if __name__ == '__main__':
    centerObj = CenterPointFromListOfCoordinates()
    f = [[37.124, 35.7856071964018], [37.12, 35.788605697151425], [37.122, 35.788605697151425], [37.126, 35.788605697151425], [37.114, 35.79160419790105], [37.116, 35.79160419790105], [37.118, 35.79160419790105], [37.128, 35.79160419790105], [37.11, 35.79460269865068], [37.112, 35.79460269865068], [37.13, 35.79460269865068], [37.106, 35.7976011994003], [37.108, 35.7976011994003], [37.132, 35.7976011994003], [37.102, 35.800599700149924], [37.104, 35.800599700149924], [37.134, 35.800599700149924], [37.096000000000004, 35.80359820089955], [37.098, 35.80359820089955], [37.1, 35.80359820089955], [37.136, 35.80359820089955], [37.092, 35.80659670164918], [37.094, 35.80659670164918], [37.138, 35.80659670164918], [37.092, 35.8095952023988], [37.14, 35.8095952023988], [37.092, 35.81259370314842], [37.142, 35.81259370314842], [37.144, 35.81259370314842], [37.092, 35.81559220389805], [37.146, 35.81559220389805], [37.148, 35.81559220389805], [37.092, 35.818590704647676], [37.15, 35.818590704647676], [37.152, 35.818590704647676], [37.153999999999996, 35.818590704647676], [37.09, 35.8215892053973], [37.156, 35.8215892053973], [37.158, 35.8215892053973], [37.09, 35.82458770614693], [37.16, 35.82458770614693], [37.162, 35.82458770614693], [37.09, 35.827586206896555], [37.164, 35.827586206896555], [37.09, 35.830584707646175], [37.166, 35.830584707646175], [37.168, 35.830584707646175], [37.088, 35.8335832083958], [37.17, 35.8335832083958], [37.086, 35.83658170914543], [37.172, 35.83658170914543], [37.084, 35.839580209895054], [37.174, 35.839580209895054], [37.176, 35.839580209895054], [37.082, 35.84257871064468], [37.178, 35.84257871064468], [37.078, 35.8455772113943], [37.08, 35.8455772113943], [37.18, 35.8455772113943], [37.182, 35.8455772113943], [37.076, 35.848575712143926], [37.184, 35.848575712143926], [37.074, 35.85157421289355], [37.186, 35.85157421289355], [37.072, 35.85457271364318], [37.188, 35.85457271364318], [37.19, 35.85457271364318], [37.072, 35.857571214392806], [37.192, 35.857571214392806], [37.072, 35.86056971514243], [37.194, 35.86056971514243], [37.072, 35.86356821589205], [37.196, 35.86356821589205], [37.198, 35.86356821589205], [37.072, 35.86656671664168], [37.2, 35.86656671664168], [37.072, 35.869565217391305], [37.202, 35.869565217391305], [37.204, 35.869565217391305], [37.072, 35.87256371814093], [37.206, 35.87256371814093], [37.072, 35.87556221889056], [37.208, 35.87556221889056], [37.072, 35.87856071964018], [37.21, 35.87856071964018], [37.212, 35.87856071964018], [37.072, 35.8815592203898], [37.214, 35.8815592203898], [37.072, 35.88455772113943], [37.216, 35.88455772113943], [37.072, 35.88755622188906], [37.218, 35.88755622188906], [37.072, 35.89055472263868], [37.22, 35.89055472263868], [37.072, 35.8935532233883], [37.222, 35.8935532233883], [37.072, 35.89655172413793], [37.224, 35.89655172413793], [37.074, 35.899550224887555], [37.226, 35.899550224887555], [37.074, 35.90254872563718], [37.228, 35.90254872563718], [37.074, 35.90554722638681], [37.23, 35.90554722638681], [37.076, 35.908545727136435], [37.232, 35.908545727136435], [37.076, 35.911544227886054], [37.234, 35.911544227886054], [37.076, 35.91454272863568], [37.236, 35.91454272863568], [37.078, 35.91754122938531], [37.238, 35.91754122938531], [37.078, 35.920539730134934], [37.24, 35.920539730134934], [37.078, 35.92353823088456], [37.242, 35.92353823088456], [37.08, 35.92653673163418], [37.244, 35.92653673163418], [37.08, 35.929535232383806], [37.246, 35.929535232383806], [37.08, 35.93253373313343], [37.248, 35.93253373313343], [37.082, 35.93553223388306], [37.25, 35.93553223388306], [37.082, 35.938530734632685], [37.084, 35.938530734632685], [37.086, 35.938530734632685], [37.252, 35.938530734632685], [37.088, 35.94152923538231], [37.09, 35.94152923538231], [37.254, 35.94152923538231], [37.092, 35.94452773613193], [37.094, 35.94452773613193], [37.096000000000004, 35.94452773613193], [37.256, 35.94452773613193], [37.098, 35.94752623688156], [37.1, 35.94752623688156], [37.102, 35.94752623688156], [37.258, 35.94752623688156], [37.104, 35.950524737631184], [37.106, 35.950524737631184], [37.26, 35.950524737631184], [37.108, 35.95352323838081], [37.11, 35.95352323838081], [37.112, 35.95352323838081], [37.262, 35.95352323838081], [37.114, 35.95652173913044], [37.264, 35.95652173913044], [37.116, 35.95952023988006], [37.266, 35.95952023988006], [37.118, 35.96251874062968], [37.268, 35.96251874062968], [37.12, 35.96551724137931], [37.27, 35.96551724137931], [37.122, 35.968515742128936], [37.272, 35.968515742128936], [37.124, 35.97151424287856], [37.274, 35.97151424287856], [37.276, 35.97151424287856], [37.126, 35.97451274362819], [37.278, 35.97451274362819], [37.128, 35.97751124437781], [37.28, 35.97751124437781], [37.128, 35.980509745127435], [37.282, 35.980509745127435], [37.13, 35.98350824587706], [37.284, 35.98350824587706], [37.132, 35.98650674662669], [37.286, 35.98650674662669], [37.134, 35.989505247376314], [37.288, 35.989505247376314], [37.29, 35.989505247376314], [37.136, 35.992503748125934], [37.292, 35.992503748125934], [37.138, 35.99550224887556], [37.294, 35.99550224887556], [37.14, 35.99850074962519], [37.296, 35.99850074962519], [37.142, 36.00149925037481], [37.144, 36.00149925037481], [37.146, 36.00149925037481], [37.298, 36.00149925037481], [37.3, 36.00149925037481], [37.148, 36.00449775112444], [37.15, 36.00449775112444], [37.152, 36.00449775112444], [37.153999999999996, 36.00449775112444], [37.302, 36.00449775112444], [37.304, 36.00449775112444], [37.156, 36.007496251874066], [37.158, 36.007496251874066], [37.16, 36.007496251874066], [37.306, 36.007496251874066], [37.308, 36.007496251874066], [37.162, 36.010494752623686], [37.164, 36.010494752623686], [37.166, 36.010494752623686], [37.31, 36.010494752623686], [37.312, 36.010494752623686], [37.168, 36.01349325337331], [37.17, 36.01349325337331], [37.172, 36.01349325337331], [37.174, 36.01349325337331], [37.314, 36.01349325337331], [37.316, 36.01349325337331], [37.176, 36.01649175412294], [37.178, 36.01649175412294], [37.18, 36.01649175412294], [37.318, 36.01649175412294], [37.32, 36.01649175412294], [37.182, 36.019490254872565], [37.322, 36.019490254872565], [37.324, 36.019490254872565], [37.182, 36.02248875562219], [37.326, 36.02248875562219], [37.328, 36.02248875562219], [37.184, 36.02548725637181], [37.33, 36.02548725637181], [37.332, 36.02548725637181], [37.184, 36.02848575712144], [37.334, 36.02848575712144], [37.336, 36.02848575712144], [37.186, 36.031484257871064], [37.338, 36.031484257871064], [37.34, 36.031484257871064], [37.186, 36.03448275862069], [37.342, 36.03448275862069], [37.186, 36.03748125937032], [37.344, 36.03748125937032], [37.188, 36.04047976011994], [37.344, 36.04047976011994], [37.188, 36.04347826086956], [37.342, 36.04347826086956], [37.188, 36.04647676161919], [37.342, 36.04647676161919], [37.19, 36.049475262368816], [37.34, 36.049475262368816], [37.19, 36.05247376311844], [37.34, 36.05247376311844], [37.192, 36.05547226386807], [37.338, 36.05547226386807], [37.192, 36.05847076461769], [37.194, 36.05847076461769], [37.338, 36.05847076461769], [37.196, 36.061469265367315], [37.336, 36.061469265367315], [37.198, 36.06446776611694], [37.2, 36.06446776611694], [37.336, 36.06446776611694], [37.202, 36.06746626686657], [37.334, 36.06746626686657], [37.202, 36.070464767616194], [37.334, 36.070464767616194], [37.204, 36.07346326836581], [37.332, 36.07346326836581], [37.204, 36.07646176911544], [37.332, 36.07646176911544], [37.204, 36.079460269865066], [37.332, 36.079460269865066], [37.206, 36.08245877061469], [37.332, 36.08245877061469], [37.206, 36.08545727136432], [37.33, 36.08545727136432], [37.206, 36.088455772113946], [37.33, 36.088455772113946], [37.206, 36.091454272863565], [37.33, 36.091454272863565], [37.208, 36.09445277361319], [37.33, 36.09445277361319], [37.208, 36.09745127436282], [37.33, 36.09745127436282], [37.208, 36.100449775112445], [37.33, 36.100449775112445], [37.21, 36.10344827586207], [37.332, 36.10344827586207], [37.21, 36.10644677661169], [37.332, 36.10644677661169], [37.212, 36.10944527736132], [37.332, 36.10944527736132], [37.212, 36.11244377811094], [37.332, 36.11244377811094], [37.212, 36.11544227886057], [37.332, 36.11544227886057], [37.214, 36.1184407796102], [37.332, 36.1184407796102], [37.214, 36.12143928035982], [37.216, 36.12143928035982], [37.218, 36.12143928035982], [37.334, 36.12143928035982], [37.22, 36.12443778110944], [37.222, 36.12443778110944], [37.224, 36.12443778110944], [37.334, 36.12443778110944], [37.226, 36.12743628185907], [37.334, 36.12743628185907], [37.226, 36.130434782608695], [37.334, 36.130434782608695], [37.226, 36.13343328335832], [37.334, 36.13343328335832], [37.226, 36.13643178410795], [37.334, 36.13643178410795], [37.226, 36.13943028485757], [37.336, 36.13943028485757], [37.226, 36.142428785607194], [37.336, 36.142428785607194], [37.226, 36.14542728635682], [37.336, 36.14542728635682], [37.226, 36.14842578710645], [37.336, 36.14842578710645], [37.226, 36.151424287856074], [37.336, 36.151424287856074], [37.226, 36.1544227886057], [37.336, 36.1544227886057], [37.226, 36.15742128935532], [37.316, 36.15742128935532], [37.318, 36.15742128935532], [37.32, 36.15742128935532], [37.322, 36.15742128935532], [37.324, 36.15742128935532], [37.336, 36.15742128935532], [37.226, 36.160419790104946], [37.234, 36.160419790104946], [37.236, 36.160419790104946], [37.238, 36.160419790104946], [37.314, 36.160419790104946], [37.326, 36.160419790104946], [37.328, 36.160419790104946], [37.33, 36.160419790104946], [37.332, 36.160419790104946], [37.334, 36.160419790104946], [37.336, 36.160419790104946], [37.226, 36.16341829085457], [37.228, 36.16341829085457], [37.23, 36.16341829085457], [37.232, 36.16341829085457], [37.24, 36.16341829085457], [37.312, 36.16341829085457], [37.336, 36.16341829085457], [37.226, 36.1664167916042], [37.238, 36.1664167916042], [37.31, 36.1664167916042], [37.238, 36.169415292353825], [37.308, 36.169415292353825], [37.238, 36.172413793103445], [37.306, 36.172413793103445], [37.236, 36.17541229385307], [37.306, 36.17541229385307], [37.236, 36.1784107946027], [37.306, 36.1784107946027], [37.236, 36.181409295352324], [37.306, 36.181409295352324], [37.234, 36.18440779610195], [37.306, 36.18440779610195], [37.234, 36.18740629685158], [37.306, 36.18740629685158], [37.236, 36.1904047976012], [37.306, 36.1904047976012], [37.236, 36.19340329835082], [37.306, 36.19340329835082], [37.238, 36.19640179910045], [37.308, 36.19640179910045], [37.238, 36.199400299850076], [37.308, 36.199400299850076], [37.24, 36.2023988005997], [37.31, 36.2023988005997], [37.24, 36.20539730134932], [37.242, 36.20539730134932], [37.244, 36.20539730134932], [37.246, 36.20539730134932], [37.248, 36.20539730134932], [37.25, 36.20539730134932], [37.252, 36.20539730134932], [37.254, 36.20539730134932], [37.256, 36.20539730134932], [37.312, 36.20539730134932], [37.258, 36.20839580209895], [37.314, 36.20839580209895], [37.258, 36.211394302848575], [37.314, 36.211394302848575], [37.256, 36.2143928035982], [37.316, 36.2143928035982], [37.256, 36.21739130434783], [37.314, 36.21739130434783], [37.256, 36.220389805097454], [37.276, 36.220389805097454], [37.312, 36.220389805097454], [37.256, 36.223388305847074], [37.274, 36.223388305847074], [37.278, 36.223388305847074], [37.28, 36.223388305847074], [37.312, 36.223388305847074], [37.254, 36.2263868065967], [37.274, 36.2263868065967], [37.282, 36.2263868065967], [37.284, 36.2263868065967], [37.31, 36.2263868065967], [37.254, 36.22938530734633], [37.274, 36.22938530734633], [37.286, 36.22938530734633], [37.288, 36.22938530734633], [37.29, 36.22938530734633], [37.308, 36.22938530734633], [37.254, 36.23238380809595], [37.274, 36.23238380809595], [37.292, 36.23238380809595], [37.294, 36.23238380809595], [37.308, 36.23238380809595], [37.254, 36.23538230884558], [37.274, 36.23538230884558], [37.296, 36.23538230884558], [37.298, 36.23538230884558], [37.306, 36.23538230884558], [37.252, 36.2383808095952], [37.274, 36.2383808095952], [37.3, 36.2383808095952], [37.302, 36.2383808095952], [37.306, 36.2383808095952], [37.252, 36.241379310344826], [37.274, 36.241379310344826], [37.304, 36.241379310344826], [37.254, 36.24437781109445], [37.274, 36.24437781109445], [37.256, 36.24737631184408], [37.258, 36.24737631184408], [37.274, 36.24737631184408], [37.26, 36.250374812593705], [37.274, 36.250374812593705], [37.262, 36.25337331334333], [37.274, 36.25337331334333], [37.264, 36.25637181409295], [37.276, 36.25637181409295], [37.266, 36.25937031484258], [37.276, 36.25937031484258], [37.268, 36.262368815592204], [37.276, 36.262368815592204], [37.27, 36.26536731634183], [37.272, 36.26536731634183], [37.276, 36.26536731634183], [37.274, 36.26836581709146], [37.278, 36.26836581709146], [37.276, 36.271364317841076], [37.278, 36.271364317841076], [37.278, 36.2743628185907]]
    # list = [[12.977324, 28.178376], [112.975782, 8.172258],[22.576876, 25.56745]]
    centre_point = centerObj.center_geolocation(f)
    # print('The centre point is: ',centre_point)
    centre_point_coordinate = millerToXY(centre_point[0],centre_point[1])
    # print('The centre point coordinate is: ',centre_point_coordinate)


    f_coordinate = []
    f_coordinate_x = []
    f_coordinate_y = []
    for i in range(len(f)):
        f_coordinate.append(millerToXY(f[i][0],f[i][1]))
    # print("The origin is: ",f_coordinate)
    for index in range(len(f_coordinate)):
        f_coordinate_x.append(f_coordinate[index][0])
        f_coordinate_y.append(f_coordinate[index][1])


    f_coordinate_2min = []
    f_coordinate_2min_x = []
    f_coordinate_2min_y = []
    for j in range(len(f)):
        point = millerToXY(f[j][0], f[j][1])
        point[0] = point[0] + 60/1000 * (point[0]-centre_point_coordinate[0])/pow(pow((point[0]-centre_point_coordinate[0]),2)+
                                                                                          pow((point[1]-centre_point_coordinate[1]),2),0.5)
        point[1] = point[1] + 60/1000 * (point[1] - centre_point_coordinate[1]) / pow(
            pow((point[0] - centre_point_coordinate[0]), 2) +
            pow((point[1] - centre_point_coordinate[1]), 2), 0.5)

        f_coordinate_2min.append(point)
    for index in range(len(f_coordinate_2min)):
        f_coordinate_2min_x.append(f_coordinate_2min[index][0])
        f_coordinate_2min_y.append(f_coordinate_2min[index][1])



    f_coordinate_5min = []
    f_coordinate_5min_x = []
    f_coordinate_5min_y = []
    for j in range(len(f)):
        point = millerToXY(f[j][0], f[j][1])
        point[0] = point[0] + 300/1000 * (point[0] - centre_point_coordinate[0]) / pow(
            pow((point[0] - centre_point_coordinate[0]), 2) +
            pow((point[1] - centre_point_coordinate[1]), 2), 0.5)
        point[1] = point[1] + 300/1000 * (point[1] - centre_point_coordinate[1]) / pow(
            pow((point[0] - centre_point_coordinate[0]), 2) +
            pow((point[1] - centre_point_coordinate[1]), 2), 0.5)

        f_coordinate_5min.append(point)
    # print(f_coordinate_5min)
    for index in range(len(f_coordinate_5min)):
        f_coordinate_5min_x.append(f_coordinate_5min[index][0])
        f_coordinate_5min_y.append(f_coordinate_5min[index][1])


    f_coordinate_10min = []
    f_coordinate_10min_x = []
    f_coordinate_10min_y = []
    for j in range(len(f)):
        point = millerToXY(f[j][0], f[j][1])
        point[0] = point[0] + 800/1000 * (point[0] - centre_point_coordinate[0]) / pow(
            pow((point[0] - centre_point_coordinate[0]), 2) +
            pow((point[1] - centre_point_coordinate[1]), 2), 0.5)
        point[1] = point[1] + 800/1000 * (point[1] - centre_point_coordinate[1]) / pow(
            pow((point[0] - centre_point_coordinate[0]), 2) +
            pow((point[1] - centre_point_coordinate[1]), 2), 0.5)

        f_coordinate_10min.append(point)
    # print(f_coordinate_10min)
    for index in range(len(f_coordinate_10min)):
        f_coordinate_10min_x.append(f_coordinate_10min[index][0])
        f_coordinate_10min_y.append(f_coordinate_10min[index][1])




 # plt.scatter(f_coordinate_2min_x,f_coordinate_2min_y, color='b',label='fire',linewidth =0.5)
    # plt.scatter(f_coordinate_5min_x,f_coordinate_5min_y,color='r',label='fire',linewidth =0.5)
    # plt.scatter(f_coordinate_10min_x,f_coordinate_10min_y,color='y',label='fire',linewidth =0.5)
    # plt.show()

    y_train = [f_coordinate_x,f_coordinate_2min_x,f_coordinate_5min_x,f_coordinate_10min_x]
    x_train = [0,2,5,10]
    x_test = [15,20,30]
    x_train = np.array(x_train).reshape(-1,1)
    x_test = np.array(x_test).reshape(-1,1)
    model = LinearRegression()
    model.fit(x_train,y_train)
    y_pre = model.predict(x_test)

    y_train_1 = [f_coordinate_y,f_coordinate_2min_y,f_coordinate_5min_y,f_coordinate_10min_y]
    x_train_1 = [0,2,5,10]
    x_test_1 = [15,20,30]
    x_train_1 = np.array(x_train_1).reshape(-1,1)
    x_test_1 = np.array(x_test_1).reshape(-1,1)
    model1 = LinearRegression()
    model1.fit(x_train_1,y_train_1)
    y_pre_1 = model1.predict(x_test_1)

    # plt.scatter(f_coordinate_2min_x, f_coordinate_2min_y, color='g', label='fire', linewidth=0.5)
    # plt.scatter(f_coordinate_5min_x,f_coordinate_5min_y,color='r',label='fire',linewidth =0.5)
    # plt.scatter(f_coordinate_10min_x,f_coordinate_10min_y,color='y',label='fire',linewidth =0.5)
    # plt.scatter(y_pre[0], y_pre_1[0], color='b', label='fire', linewidth=0.5)
    # plt.scatter(y_pre[1], y_pre_1[1],color='r',label='fire',linewidth =0.5)
    # plt.scatter(y_pre[2], y_pre_1[2],color='y',label='fire',linewidth =0.5)
    # plt.show()

    f_coordinate_15min = []
    F_coordinate_15min = []
    f_coordinate_20min = []
    f_coordinate_30min = []
    for index in range(len(y_pre[0])):
        f_coordinate_15min.append(millerToLonLat(y_pre[0][index],y_pre_1[0][index]))
    f_coordinate_15min = pointsample(f_coordinate_15min)
    length = len(f_coordinate_15min)
    for i in range(0,length):
        F_coordinate_15min.append(f_coordinate_15min[i][0])
        F_coordinate_15min.append(f_coordinate_15min[i][1])
    print(F_coordinate_15min)
    for index in range(len(y_pre[1])):
        f_coordinate_20min.append(millerToLonLat(y_pre[1][index], y_pre_1[1][index]))
    # print("20 min is:", f_coordinate_20min)

    for index in range(len(y_pre[2])):
        f_coordinate_30min.append(millerToLonLat(y_pre[2][index], y_pre_1[2][index]))
    # print("30 min is:", f_coordinate_30min)








