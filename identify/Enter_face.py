import cv2 as cv
from cv2 import face as Face
import os
import start
import numpy as np
from PIL import Image


def face_detect_domo(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    face_detect = cv.CascadeClassifier(
        r'D:\anaconda3\envs\flaskproject_classic\lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')
    face = face_detect.detectMultiScale(gray, 1.02015, 5, 0, (100, 100), (300, 300))
    for x, y, w, h in face:
        cv.rectangle(img, (x, y), (x + w, y + h), color=(0, 0, 255), thickness=2)
    cv.imshow('result', img)


def getImageAndLabels(path):
    # 储存人脸数据
    faceSamples = []
    # 存储姓名数据
    ids = []
    # 获取该目录下所有图片路径
    imgePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # 加载分类器
    face_dector=cv.CascadeClassifier(
        r'D:\anaconda3\envs\flaskproject_classic\lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')
    for i in imgePaths:
        #以灰度图的方式打开图片
        PIL_img=Image.open(i).convert('L')
        #将图片转化为数组，以黑白深浅
        img_numpy=np.array(PIL_img,'uint8')
        #获取人脸特征
        faces = face_dector.detectMultiScale(img_numpy)
        id=int(os.path.split(i)[1].split('.')[0])
        #预防无面容的情况
        for x,y,w,h in faces:
            ids.append(id)
            faceSamples.append(img_numpy[y:y+h,x:x+w])
        print('id',id)
        print('fs:',faceSamples)
    return faceSamples,ids

#人脸录入
def Enter_faces(name):
    # 循环捕获摄像头的帧
    path = './face_img/id'  # 输入文件夹地址
    files = os.listdir(path)  # 读入文件夹
    num_png = len(files)  # 统计文件夹中的文件个数

    cap = cv.VideoCapture(0)
    # 检查摄像头是否成功打开
    if not cap.isOpened():
        print("无法打开摄像头")
        exit()
    while True:
        # 读取一帧
        ret, frame = cap.read()
        # 如果读取成功，显示帧
        print(ret, frame)
        if ret:
            face_detect_domo(frame)
            # 按s保存图片
            if cv.waitKey(1) & 0xFF == ord('s'):
                img_each = './face_img/id/' + str(num_png)+'.'+name + '.png'
                cv.imwrite(img_each, frame)
                print('已经保存至', img_each)
                print(num_png)
                num_png = num_png + 1
                break
    # 释放摄像头资源
    cap.release()
    # 关闭所有窗口
    cv.destroyAllWindows()

    faces, ids = getImageAndLabels('./face_img/id')
    recognizer = Face.LBPHFaceRecognizer_create()
    recognizer.train(faces, np.array(ids))
    recognizer.write('trainer/trainer.yml')

# Enter_faces(name)
# start.identify()