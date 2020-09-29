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
#获取图形轮廓
def getContours(img):
    #获取所有的图形轮廓，并存储
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)#检索图形轮廓
    #遍历循环每一个轮廓
    for cnt in contours:
        #计算轮廓面积
        area = cv2.contourArea(cnt)
        # print(area)
        #画边框线
        if area > 500:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
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
            #通过角的个数判断形状
            if objCor == 3:objectType = "Tri"
            elif objCor == 4:
                #判断四边形类型
                aspRatio = w/float(h)
                if aspRatio > 0.95 and aspRatio < 1.05:objectType = "Square"
                else:objectType = "Rectangle"
            elif objCor > 4:objectType = "Circle"
            else:objectType = "None"
            # 给图形画边框
            cv2.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.putText(imgContour,objectType,(x+(w//2)-10,y+(h//2)-10),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,0),2)

#读取图片
path = 'Resources/shapes.png'
img = cv2.imread(path)
#复制图像
imgContour = img.copy()
#检测每一个矩形，并将其分类，显示面积，端点个数
#BGR2GRAY 图片灰度处理
imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#GaussianBlur 模糊
imgBlur = cv2.GaussianBlur(imgGray,(7,7),1)
#边缘检测
imgCanny = cv2.Canny(img,100,100)
#获取轮廓
getContours(imgCanny)
#创建空白图片
imgBlank = np.zeros_like(img)
#图片整合
imgStack = stackImages(0.5,([img,imgGray,imgBlank],[imgBlur,imgCanny,imgContour]))
# cv2.imshow("Original",img)
# cv2.imshow("Gray",imgGray)
# cv2.imshow("Blur",imgBlur)
cv2.imshow("imgStack",imgStack)
cv2.waitKey(0)