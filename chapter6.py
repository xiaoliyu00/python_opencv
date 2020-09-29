#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：lucky
# albert time:2020/9/5
import cv2
import numpy as np

#将图像结合在一起
img = cv2.imread('Resources/lena.png')

#使用水平堆栈功能，将其进行自身堆叠
imgHor = np.hstack((img,img))

#使用竖直堆叠功能，将其进行自身堆叠
imgVer = np.vstack((img,img))

#展示图片
cv2.imshow("Horizontal",imgHor)
cv2.imshow("Vertical",imgVer)

cv2.waitKey(0)