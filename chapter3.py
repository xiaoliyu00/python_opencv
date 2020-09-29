#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：lucky
# albert time:2020/9/5
import cv2
#read image
img = cv2.imread("Resources/lambo.png")
#检查图像的尺寸
# print(img.shape)

#调整图像大小,必须先定义宽度，再定义高度
imgResize = cv2.resize(img,(300,200))

#裁剪图像,图像本身为矩阵
imgCropped = img[0:200,200:500]

cv2.imshow("Image",img)
cv2.imshow("Image Resize",imgResize)
cv2.imshow("Image Cropped",imgCropped)

cv2.waitKey(0)