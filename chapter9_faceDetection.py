#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：lucky
# albert time:2020/9/7
import cv2

#导入人脸识别工具
faceCascade = cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")
#读取图片
img = cv2.imread("Resources/lena.png")
#图片灰度操作
imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

#人脸多级检测
faces = faceCascade.detectMultiScale(imgGray,1.3,3)

for (x,y,w,h) in faces:
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

cv2.imshow("Result",img)
cv2.waitKey(0)
