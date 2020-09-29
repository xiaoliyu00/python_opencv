#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：lucky
# albert time:2020/9/5
import cv2
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

while True:
    success,img = cap.read()
    cv2.imshow("Video",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break