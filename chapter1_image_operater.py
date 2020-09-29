#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：lucky
# albert time:2020/9/5
import cv2

print('Packeage Imported')

#read image
img = cv2.imread("Resources/lena.png")

# #display image
# cv2.imshow("Output",img)

#添加延迟
cv2.waitKey(0)