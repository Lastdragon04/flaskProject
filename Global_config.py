from flask import url_for
def get_System_logo():
    return url_for('static',filename='img/logo.png')
System_name = '智能家具控制系统'
XiaoY = "../static/img/小Y1代.png"
face_img_path='./static/img/face_img/id'
xml_path=r'D:\anaconda3\envs\flaskproject_classic\lib\site-packages\cv2\data\haarcascade_frontalface_default.xml'
yml_path='./identify/trainer/trainer.yml'
sql_name='root'
sql_password='123654'
sql_base='reptile_sys'
Mail='1692930439@qq.com'
SECRET='gmuenpwstifpechf'
