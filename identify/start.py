import cv2
import numpy as np
import os
# coding=utf-8
import urllib
import urllib.request
import hashlib


# 加载训练数据集文件

names = []
Right = {}
recogizer = cv2.face.LBPHFaceRecognizer_create()
recogizer.read('./trainer/trainer.yml')


# 准备识别的图片
def face_detect_demo(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转换为灰度
    face_detector = cv2.CascadeClassifier(
        r'D:\anaconda3\envs\flaskproject_classic\lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')
    face = face_detector.detectMultiScale(gray, 1.1, 5, cv2.CASCADE_SCALE_IMAGE, (100, 100), (300, 300))
    # face=face_detector.detectMultiScale(gray)
    temp=0
    for x, y, w, h in face:
        cv2.rectangle(img, (x, y), (x + w, y + h), color=(0, 0, 255), thickness=2)
        cv2.circle(img, center=(x + w // 2, y + h // 2), radius=w // 2, color=(0, 255, 0), thickness=1)
        # 人脸识别
        ids, confidence = recogizer.predict(gray[y:y + h, x:x + w])
        print(confidence)
        # print('标签id:',ids,'置信评分：', confidence)
        if confidence > 64:
            cv2.putText(img, 'unkonw', (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 1)
        else:
            cv2.putText(img, str(names[ids]), (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 1)
            temp=ids
    cv2.imshow('result', img)
    if temp==0:
        return 'unknown'
    else:
        return names[temp]

def get_name():
    path = './face_img/id/'
    # names = []
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    for imagePath in imagePaths:
        name = str(os.path.split(imagePath)[1].split('.', 2)[1])
        names.append(name)


def identify():
    global Right
    temp_name = ''
    cap = cv2.VideoCapture(0)
    get_name()
    print(names)
    while True:
        flag, frame = cap.read()
        if not flag:
            break
        name=face_detect_demo(frame)
        if name!='unknown':
            try:
                if Right[name]!=None and temp_name==name:
                    Right[name]=Right[name]+1
                else:
                    Right={}
                if Right[name] > 100:
                    break
            except KeyError:
                Right[name]=0
            temp_name = name
        else:
            Right={}
        if ord('q') == cv2.waitKey(10):
            break
        print(Right)

    cv2.destroyAllWindows()
    cap.release()
# print(names)
