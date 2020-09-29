#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：lucky
# albert time:2020/9/7
import cv2
import numpy as np

#通过网络摄像头获取视频内容
cap = cv2.VideoCapture(0)

#定义视频窗口大小
frameWidth = 640
frameHeight = 480
#宽度
cap.set(3,frameWidth)
#高度
cap.set(4,frameHeight)
#亮度
cap.set(10,100)

#已经检测完成的颜色属性
myColors = [[5,107,0,19,255,255],
            [133,56,0,159,156,255],
            [57,76,0,100,255,255],
            [90,48,0,118,255,255]]
#色号，每一行代表一种颜色，之后用来画图
myColorValues = [[51,153,255],          ## BGR
                 [255,0,255],
                 [0,255,0],
                 [255,0,0]]

# [x,y,colorId]
myPoints = []

#获取位置并标记，存储在newPoints
def findColor(img,myColors,myColorValues):
    # 将图片转化为HSV
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for color in myColors:
    #利用修改的数值对图片进行相关操作
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x,y = getContours(mask)
        cv2.circle(imgResult,(x,y),10,myColorValues[count],cv2.FILLED)
        if x != 0 and y != 0:
            newPoints.append([x,y,count])
        count += 1
        # cv2.imshow(str(color[0]),mask)
    return newPoints

#获取图形轮廓
def getContours(img):
    #获取所有的图形轮廓，并存储
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)#检索图形轮廓
    x,y,w,h = 0,0,0,0
    #遍历循环每一个轮廓
    for cnt in contours:
        #计算轮廓面积
        area = cv2.contourArea(cnt)
        # print(area)
        #画边框线
        if area > 500:
            cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            #计算弧长
            peri = cv2.arcLength(cnt,True)
            # print(peri)
            #计算角的个数
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            # print(approx)
            # print(len(approx))
            #角的个数
            objCor =len(approx)
            #x,y,宽，高
            x,y,w,h = cv2.boundingRect(approx)
    return x+w//2,y

#依据检测颜色画线
def drawOnCanvas(myPoints,myColorValues):
    for point in myPoints:
        cv2.circle(imgResult,(point[0],point[1]),10,myColorValues[point[2]],cv2.FILLED)

while True:
    success,img = cap.read()
    imgResult = img.copy()
    newPoints = findColor(img,myColors,myColorValues)

    if len(newPoints) != 0:
       for newPoint in newPoints:
           myPoints.append(newPoint)

    if len(myPoints) != 0:
        drawOnCanvas(myPoints,myColorValues)

    cv2.imshow("Video",imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break