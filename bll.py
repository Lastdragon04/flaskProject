from string import ascii_letters, digits
from random import sample
from numpy import frombuffer,uint8
from cv2 import imdecode,IMREAD_COLOR
from base64 import b64decode

def create_captcha(number):
    letters = ascii_letters + digits
    captcha = "".join(sample(letters, number))
    return captcha

def tran_channel16to1(data):
    encoded_data = data.split(",")[1]
    nparr = frombuffer(b64decode(encoded_data), uint8)
    # # 人脸识别部分
    image = imdecode(nparr, IMREAD_COLOR)
    return image