#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：lucky
# albert time:2020/9/5
import cv2
import numpy as np
#学习如何在图像上绘制形状

#创建黑色图像
img_balck = np.zeros((512,512))
# print(img.shape)
#创建彩色图像
img_color = np.zeros((512,512,3),np.uint8)
img_color[200:300,100:300] = 255,0,0 #蓝色

#画线
#                  起点   终点      颜色   通道数
cv2.line(img_color,(0,0),(300,300),(0,255,0),3)

#画矩形
cv2.rectangle(img_color,(0,0),(200,200),(0,255,0),3)
cv2.rectangle(img_color,(0,0),(200,200),(0,255,0),cv2.FILLED)#颜色填充

#画圆
cv2.circle(img_color,(300,300),50,(255,255,0),3)

#添加文本
cv2.putText(img_color,"OPENCV",(300,100),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),1)
cv2.imshow("image",img_color)
cv2.waitKey(0)