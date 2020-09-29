#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：lucky
# albert time:2020/9/7
import cv2
import numpy as np

#任意修改图像大小
#将图像结合在一起
def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

def empty(a):
    pass

#读取图片
path = 'Resources/lambo.png'
#新建跟踪栏窗口，用来测试颜色，通过调节可以找到颜色的范围
cv2.namedWindow("TrackBars")
#定义大小
cv2.resizeWindow("TrackBars",640,240)

#创建并使用跟踪栏功能
#可以自己修改相关数值
#hue 色调（度）色调是指图像的相对明暗程度，在彩色图像上表现为颜色。
cv2.createTrackbar("Hue Min","TrackBars",0,179,empty)
cv2.createTrackbar("Hue Max","TrackBars",19,179,empty)
#saturation 饱和度饱和度是指某种颜色的量的多少，即鲜艳程度，也可以说是强度或纯度。
cv2.createTrackbar("Sat Min","TrackBars",1,255,empty)
cv2.createTrackbar("Sat Max","TrackBars",255,255,empty)
#value是指（bai色彩的）浓淡关系度，敏感程度或（艺术作品的）明暗相称。
cv2.createTrackbar("Val Min","TrackBars",122,255,empty)
cv2.createTrackbar("Val Max","TrackBars",255,255,empty)

while True:
    img = cv2.imread(path)
    cv2.putText(img, "imgOriginal", (300, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)

    #目标：检测橙色
    #将图片转化为HSV
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    cv2.putText(imgHSV, "imgHSV", (300, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
    #获取图片各项指标的变化
    h_min = cv2.getTrackbarPos("Hue Min","TrackBars")
    h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
    s_min = cv2.getTrackbarPos("Sat Min","TrackBars")
    s_max = cv2.getTrackbarPos("Sat Max","TrackBars")
    v_min = cv2.getTrackbarPos("Val Min","TrackBars")
    v_max = cv2.getTrackbarPos("Val Max","TrackBars")
    print(h_min,h_max,s_min,s_max,v_min,v_max)

    #利用修改的数值对图片进行相关操作
    lower = np.array([h_min,s_min,v_min])
    upper = np.array([h_max,s_max,v_max])
    mask = cv2.inRange(imgHSV, lower, upper)
    cv2.putText(mask, "mask", (300, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
    # 创建新图片，用以存储检测结果
    #即在原始图像中显示出橙色的位置
    #方法是原始图片与检测mask计算交集
    imgResult = cv2.bitwise_and(img,img,mask = mask)
    cv2.putText(imgResult, "imgResult", (300, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
    #展示图片
    # cv2.imshow("original",img)
    # cv2.imshow("imgHSV",imgHSV)
    # cv2.imshow("Mask",mask)
    # cv2.imshow("Result", imgResult)
    imgStack = stackImages(0.5,([img,imgHSV],[mask,imgResult]))
    cv2.imshow("imgStack",imgStack)
    cv2.waitKey(1)