#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：lucky
# albert time:2020/9/5
import cv2
import numpy as np
#读取图像
img = cv2.imread("Resources/cards.jpg")
#定义宽 高
width,height = 250,250
#取图像
pts1 = np.float32([[111,219],[287,188],[154,482],[352,440]])
#参考
pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])
matrix = cv2.getPerspectiveTransform(pts1,pts2)
#将取出的图像尽可能输出平面图
imgOutput = cv2.warpPerspective(img,matrix,(width,height))

#图像显示
cv2.imshow("image",img)
cv2.imshow("image Output",imgOutput)
#延迟
cv2.waitKey(0)
