import cv2 as cv
from cv2 import face as Face
import numpy as np
from PIL import Image
import os
import Global_config

def face_detect_domo(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    face_detect = cv.CascadeClassifier(
        Global_config.xml_path)
    face = face_detect.detectMultiScale(gray, 1.02015, 5, 0, (100, 100), (300, 300))
    for x, y, w, h in face:
        cv.rectangle(img, (x, y), (x + w, y + h), color=(0, 0, 255), thickness=2)


def getImageAndLabels(path):
    # 储存人脸数据
    faceSamples = []
    # 存储姓名数据
    ids = []
    # 获取该目录下所有图片路径
    imgePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # 加载分类器
    face_dector = cv.CascadeClassifier(
        r'D:\anaconda3\envs\flaskproject_classic\lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')
    for i in imgePaths:
        # 以灰度图的方式打开图片
        PIL_img = Image.open(i).convert('L')
        # 将图片转化为数组，以黑白深浅
        img_numpy = np.array(PIL_img, 'uint8')
        # 获取人脸特征
        faces = face_dector.detectMultiScale(img_numpy)
        id = int(os.path.split(i)[1].split('.')[0])
        # 预防无面容的情况
        for x, y, w, h in faces:
            ids.append(id)
            faceSamples.append(img_numpy[y:y + h, x:x + w])
    return faceSamples, ids,len(faces)


# 人脸录入
def Enter_faces(img_path,id_path,trainer_path):
    # print('img_path=',img_path)
    image = cv.imread(img_path)  # '../identify/face_img/id/1.zck.png'
    # print(image)
    face_detect_domo(image)
    cv.imencode('.jpg', image)[1].tofile(img_path)
    faces, ids,faces_num = getImageAndLabels(id_path)
    if faces_num==1:
        print('成功')
        print('生成特征文件')
        recognizer = Face.LBPHFaceRecognizer_create()
        recognizer.train(faces, np.array(ids))
        recognizer.write(trainer_path)
        return 1
    elif faces_num==0:
        print('未生成特征文件，回滚')
        return 0
    else:
        print('未生成特征文件，回滚')
        return 2


# start.identify()
