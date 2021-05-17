import cv2
import numpy as np
import math
from PIL import Image
import matplotlib.pyplot as plt


def PixelBoundary(filepath):
    img = Image.open(filepath)
    boundary = []
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            px = img.getpixel((x,y))
            if px[1] == 255:
                left_px = img.getpixel((x - 1, y))
                right_px = img.getpixel((x + 1, y))
                top_px = img.getpixel((x, y - 1))
                bottom_px = img.getpixel((x, y + 1))
                if left_px[1] == 0 or right_px[1] == 0 or top_px[1] == 0 or bottom_px[1] == 0:
                    pixel_location = [x, y]
                    boundary.append(pixel_location)
    return boundary, img.size[0], img.size[1]

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
    return [pixel_longitude, pixel_latitude]


# 计算整个火际线像素点的经纬度
def FireBoundary(filepath, picturelocation, flyAngle, height, sideAngle,
                  backwardAngle, cameraAngle, planePitchAngle, cameraPitchAngle):
    boundary, picWidth, picLength = PixelBoundary(filepath)
    fire_boundary = []
    for pixel in boundary:
        pixel_boundary_value = PixelLocation(pixel, picturelocation, picWidth, picLength, flyAngle, height, sideAngle,
                  backwardAngle, cameraAngle, planePitchAngle, cameraPitchAngle)
        fire_boundary.append(pixel_boundary_value)
    return fire_boundary


# 计算火情面积
def FireArea(filepath, flyAngle, height, sideAngle, backwardAngle, cameraAngle, planePitchAngle, cameraPitchAngle):
    img = cv2.imread(filepath)
    fire_num = 0
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            px = img[x, y]
            if px[2] == 128:
                fire_num = fire_num + 1
    img_area = img.shape[0] * img.shape[1]
    length, width, flyAngle = BasicInformation(flyAngle, height, sideAngle, backwardAngle,
                                                                  cameraAngle, planePitchAngle, cameraPitchAngle)
    fire_areas = (fire_num / img_area) * length * width
    return fire_areas


# pic_path = "label6.png"
# fire_boundary = []
# fire_boundary_x = []
# fire_boundary_y = []
# boundary = PixelBoundary(pic_path)
# image = cv2.imread(pic_path)
# for i in boundary:
#     pixel_boundary_value = PixelLocation(i, [[35, 36]], image.shape[0], image.shape[1], 60, 111, 30, 60, 15, 15, -19)
#     fire_boundary.append(pixel_boundary_value)
#     fire_boundary_x.append(pixel_boundary_value[0])
#     fire_boundary_y.append(pixel_boundary_value[1])
# fire_area = FireArea(pic_path, 60, 111, 30, 60, 15, 15, -19)
#
# plt.scatter(fire_boundary_x, fire_boundary_y, color='g', label='fire', linewidth=0.1)
# plt.show()
# print(fire_boundary)
# print(fire_area)
