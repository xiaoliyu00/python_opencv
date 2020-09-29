#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：lucky
# albert time:2020/9/5
import cv2
import numpy as np
print('Packeage Imported')

#read image
img = cv2.imread("Resources/lena.png")
#kernal size
kernal = np.ones((5,5),np.uint8)
#Basic function
#BGR2GRAY
imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

#GaussianBlur 模糊
imgBlur = cv2.GaussianBlur(imgGray,(7,7),0)

#边缘检测
imgCanny = cv2.Canny(img,100,100)

#膨胀
imgDialation = cv2.dilate(imgCanny,kernal,iterations=5)

# 侵蚀
imgEroded = cv2.erode(imgCanny,kernal,iterations=1)

# cv2.imshow("Gray Image",imgGray)
# cv2.imshow("Blur Image",imgBlur)
cv2.imshow("imgCanny  Image",imgCanny)
cv2.imshow("Dialation Image",imgDialation)
cv2.imshow("Eroded Image",imgEroded)
# #display image
# cv2.imshow("Output",img)

#添加延迟
cv2.waitKey(0)