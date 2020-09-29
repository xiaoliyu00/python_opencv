#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：lucky
# albert time:2020/9/5
import cv2

#获取视频
cap = cv2.VideoCapture("Resources/test_video.mp4")

#因为视频是由一系列图线组成，所以需要读取所有的图像，也就是每一帧的获取
#这里使用while循环遍历每一帧图像
while True:
    success,img = cap.read()
    cv2.imshow("Video",img)
    #按键q可以用来关闭进程
    if cv2.waitKey(1) & 0xff == ord('q'):
        break