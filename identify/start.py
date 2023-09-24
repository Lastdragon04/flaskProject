import cv2
import numpy as np
import os
# coding=utf-8
from PIL import Image, ImageFont, ImageDraw
from Model import UserModel
# 加载训练数据集文件
import Global_config
names = []
Right = {}


# def cv2AddChineseText(img, text, position, textColor=(0, 255, 0), textSize=30):
#     if isinstance(img, np.ndarray):  # 判断是否OpenCV图片类型
#         img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
#     # 创建一个可以在给定图像上绘图的对象
#     draw = ImageDraw.Draw(img)
#     # 字体的格式
#     fontStyle = ImageFont.truetype(
#         r"../static/identify/simsun.ttc", textSize, encoding="utf-8")
#     # 绘制文本
#     draw.text(position, text, textColor, font=fontStyle)
#     # 转换回OpenCV格式
#     return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


# 准备识别的图片
def face_detect_demo(img,Email_list):#./trainer/trainer.yml
    global names
    names=Email_list
    recogizer = cv2.face.LBPHFaceRecognizer_create()
    recogizer.read(Global_config.yml_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转换为灰度
    face_detector = cv2.CascadeClassifier(
        Global_config.xml_path)
    face = face_detector.detectMultiScale(gray, 1.1, 5, cv2.CASCADE_SCALE_IMAGE, (100, 100), (300, 300))
    # face=face_detector.detectMultiScale(gray)
    temp = -1
    for x, y, w, h in face:
        cv2.rectangle(img, (x, y), (x + w, y + h), color=(0, 0, 255), thickness=2)
        cv2.circle(img, center=(x + w // 2, y + h // 2), radius=w // 2, color=(0, 255, 0), thickness=1)
        # 人脸识别
        ids, confidence = recogizer.predict(gray[y:y + h, x:x + w])
        print(confidence)
        # print('标签id:',ids,'置信评分：', confidence)
        if confidence > 60:
            cv2.putText(img, 'Unknown', (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 1)
            temp=-1
        else:
            cv2.putText(img, 'Identifying', (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 1)
            temp = ids
    # print(temp)
    if temp == -1:
        return 'unknown'
    else:
        return names[temp-1]




# def identify(namelist):
#     global Right,names
#     names=namelist
#     temp_name = ''
#     cap = cv2.VideoCapture(0)
#     print(names)
#     while True:
#         flag, frame = cap.read()
#         if not flag:
#             break
#         name = face_detect_demo(frame)
#         if name != 'unknown':
#             try:
#                 if Right[name] != None and temp_name == name:
#                     Right[name] = Right[name] + 1
#                 else:
#                     Right = {}
#                 if Right[name] > 100:
#                     break
#             except KeyError:
#                 Right[name] = 0
#             temp_name = name
#         else:
#             Right = {}
#         if ord('q') == cv2.waitKey(10):
#             break
#         print(Right)
#
#     cv2.destroyAllWindows()
#     cap.release()