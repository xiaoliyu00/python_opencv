#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：lucky
# albert time:2020/9/8
import cv2

#############################################
#设置窗口大小
frameWidth = 640
frameHeight = 480
#使用级联算法检测车牌号码
nPlateCascade = cv2.CascadeClassifier("Resources/haarcascade_russian_plate_number.xml")
#待检测最小面积
minArea = 200
#车牌标记颜色
color = (255,0,255)
###############################################
#读取视频
cap = cv2.VideoCapture("Resources/video12.mp4")
#设置窗口大小
cap.set(3, frameWidth)
cap.set(4, frameHeight)
#设置亮度
cap.set(10,150)
count = 0

while True:
    success, img = cap.read()
    #图像灰度处理
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    numberPlates = nPlateCascade.detectMultiScale(imgGray, 1.1, 10)
    #筛选合适的车牌
    for (x, y,w, h) in numberPlates:
        area = w*h
        if area >minArea:
            #标记框
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)
            #标记
            cv2.putText(img,"Number Plate",(x,y-5),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL,1,color,2)
            imgRoi = img[y:y+h,x:x+w]
            cv2.imshow("ROI", imgRoi)

    cv2.imshow("Result", img)

    if cv2.waitKey(1) & 0xFF == ord('s'):
        #将结果保存
        cv2.imwrite("Resources/Scanned/NoPlate_"+str(count)+".jpg",imgRoi)
        cv2.rectangle(img,(0,200),(640,300),(0,255,0),cv2.FILLED)
        cv2.putText(img,"Scan Saved",(150,265),cv2.FONT_HERSHEY_DUPLEX,
                    2,(0,0,255),2)
        cv2.imshow("Result",img)
        cv2.waitKey(500)
        count +=1