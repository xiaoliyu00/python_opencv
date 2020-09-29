#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：lucky
# albert time:2020/9/8
import cv2
import numpy as np

#通过网络摄像头获取视频内容
# cap = cv2.VideoCapture(0)

#定义视频窗口大小
frameWidth = 540
frameHeight = 640
# #宽度
# cap.set(3,frameWidth)
# #高度
# cap.set(4,frameHeight)
# #亮度
# cap.set(10,150)

#对视频进行预处理
def preProcessing(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # GaussianBlur 模糊
    imgBlur = cv2.GaussianBlur(imgGray,(5,5),1)
    # 边缘检测
    imgCanny = cv2.Canny(img,200,200)
    kernal = np.ones((5,5))
    # 膨胀
    imgDialation = cv2.dilate(imgCanny, kernal, iterations=2)
    # 侵蚀
    imgEroded = cv2.erode(imgDialation, kernal, iterations=1)
    return  imgEroded

#获取图形轮廓
def getContours(img):
    biggest = np.array([])
    maxArea = 0
    #获取所有的图形轮廓，并存储
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)#检索图形轮廓
    #遍历循环每一个轮廓
    for cnt in contours:
        #计算轮廓面积
        area = cv2.contourArea(cnt)
        # print(area)
        #画边框线
        if area > 5000:
            # cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            #计算弧长
            peri = cv2.arcLength(cnt,True)
            # print(peri)
            #计算角的个数
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            #查找最大面积
            if area > maxArea and len(approx) == 4:
                biggest = approx
                maxArea = area
    cv2.drawContours(imgContour, biggest, -1, (255, 0, 0),20)
    return biggest

#重新排序点位点
def reorder(myPoints):
    #将原本（4,2,1）=》（4,2）
    myPoints = myPoints.reshape((4,2))
    myPointsNew = np.zeros((4,1,2),np.int32)
    #标记点数求和
    add = myPoints.sum(1)
    # print("add",add)
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    # print("NewPoints",myPointsNew)
    #diff output a[n] - a[n-1]
    diff = np.diff(myPoints,axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    # print("NewPoints",myPointsNew)
    return  myPointsNew

def getWarp(img,biggest):
    biggest = reorder(biggest)
    # 取图像
    pts1 = np.float32(biggest)
    # 参考
    pts2 = np.float32([[0, 0], [frameWidth, 0], [0, frameHeight], [frameWidth, frameHeight]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    # 将取出的图像尽可能输出平面图
    imgOutput = cv2.warpPerspective(img, matrix, (frameWidth, frameHeight))
    #裁剪图像
    imgCropped = imgOutput[20:imgOutput.shape[0] - 20, 20:imgOutput.shape[1] - 20]
    imgCropped = cv2.resize(imgCropped, (frameWidth, frameHeight))
    return imgCropped

#将多张图片整合后输出
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

while True:
    # success,img = cap.read()
    img = cv2.imread("Resources/1.jpg")
    img = cv2.resize(img,(frameWidth,frameHeight))
    imgContour = img.copy()
    imgThres = preProcessing(img)
    biggest = getContours(imgThres)
    if biggest.size != 0:
        imgWarped = getWarp(img, biggest)
        imageArray = ([img,imgThres],
                   [imgContour,imgWarped])
        # imageArray = ([imgContour, imgWarped])
        # cv2.imshow("ImageWarped", imgWarped)
    else:
         imageArray = ([img, imgThres],
                      [img, img])
        # imageArray = ([imgContour, img])

    stackedImages = stackImages(0.6, imageArray)
    cv2.imshow("WorkFlow", stackedImages)
    cv2.waitKey(0)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break