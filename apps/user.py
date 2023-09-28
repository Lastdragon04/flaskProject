import base64
from io import BytesIO
from PIL import Image
from flask import Blueprint, request, session, jsonify, redirect, url_for,render_template
from smtplib import SMTPServerDisconnected
from werkzeug.security import generate_password_hash, check_password_hash
from bll import create_captcha
from exts import db
from Mail import send_captcha
from SQL_Defence import SQL_defend
from Model import UserModel
from identify.Enter_face import Enter_faces
import os
from check import check_login

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/register1_send_captcha', methods=['POST'])
def register1():
    captcha = create_captcha(6)
    Register_Email = request.form.getlist('Register_Email')
    Register_Username = request.form['Register_Username']
    User = UserModel.query.filter_by(Username=Register_Username).first()
    Mail = UserModel.query.filter_by(Email=Register_Email[0]).first()
    print('User:', User)
    print('Mail:', Mail)
    if User:
        return 'repeat1'
    if Mail:
        return 'repeat2'
    elif not User and not Mail:
        try:
            X = send_captcha(Register_Username, captcha, Register_Email)
            session['Register_Email'] = Register_Email[0]
            session['Register_Username'] = Register_Username
            session['captcha'] = captcha
            return 'OK'
        except SMTPServerDisconnected:
            return 'Wrong'


@bp.route("/register2_get_captcha", methods=['POST'])
def register2_get_captcha():
    if request.method == 'POST':
        captcha = request.form['captcha']
        try:
            server_captcha = session.get('captcha')
        except KeyError:
            return 'Error'
        if captcha != server_captcha:
            return 'NO'
        else:
            return 'OK'


@bp.route("/register3", methods=['POST'])
def register3():
    if request.method == 'POST':
        try:
            if session['captcha'] and session['Register_Email'] and session['Register_Username']:
                password = request.form['password']
                session['password'] = password
                return 'OK'
        except KeyError:
            return '我真草泥马，老子小网站你攻击你妈攻击,他妈学了地点爬虫就给你牛逼死了哈，回去好好再学学你那javascript，有种来攻击老子服务器'


@bp.route("/register4_enter_face", methods=['POST'])
def register4_enter_face():
    if request.method == 'POST':
        captcha = session.get('captcha')
        Username = session.get('Register_Username')
        Email = session.get('Register_Email')
        password = session.get('password')
        if captcha and Username and Email and password:
            data_url = request.form['file']  # Get the Data URL from FormData
            print(data_url)
            content_type, base64_data = data_url.split(",")[0], data_url.split(",")[1]
            if 'base64' not in content_type:
                return jsonify({"error": "Invalid Data URL format."}), 400
            decoded_image = base64.b64decode(base64_data)
            image = Image.open(BytesIO(decoded_image))
            print(image)
            # Save or process the image as required
            imagePaths = [os.path.join(r'.\identify\face_img\id', f) for f in os.listdir(r'.\identify\face_img\id')]
            print(len(imagePaths))
            num = str(len(imagePaths) + 1)
            path = r'.\identify\face_img\id\%s.png' % (num)
            path2 = r'.\identify\face_img\id'
            path3 = r'.\identify\trainer\trainer.yml'
            image.save(path)
            flag = Enter_faces(path, path2, path3)
            if flag==1:
                print('检测到一张人脸')
                user = UserModel(Email=Email, Username=Username, Password=generate_password_hash(password),
                                 Face_path=str(path))
                db.session.add(user)
                db.session.commit()
                User = UserModel.query.filter_by(Email=Email).first()
                session.pop('captcha')
                session.pop('Register_Email')
                session.pop('Register_Username')
                session.pop('password')
                return jsonify({"message": "File processed successfully."}), 200
            elif flag > 1:
                os.remove(path)
                print('过多人脸')
                return 'Too much'
            else:
                os.remove(path)
                return 'None'
        else:
            return 'ERROR'


@bp.route("/login", methods=['POST'])
def Login():
    if request.method == 'POST':
        Password = request.form['Password']
        Email = request.form['Email']
        print(Password)
        try:
            if Email==session.get('Email'):
                return 'ATTACK'
        except KeyError:
            pass
        Email_Defence = SQL_defend(Password)
        if Email_Defence:
            user = UserModel.query.filter_by(Email=Email).first()
            print(user)
            if not user:
                return 'None'
            else:
                if check_password_hash(user.Password, Password):
                    print('session设置成功')
                    session['Email'] = Email
                    session['Username'] = user.Username
                    return 'OK'
                else:
                    return 'Error'
        else:
            return 'Wrong'


@bp.route("/logout", methods=['GET'])
def logout():
    if request.method == 'GET':
        try:
            session.pop('Username')
            session.pop('Email')
            return redirect('/')
        except KeyError:
            return 'ERROR'


@bp.route("/forget_password1", methods=['POST'])
def forget_password1():
    if request.method == 'POST':
        print('找回密码')
        Email = request.form['Email_onforget']
        temp = SQL_defend(Email)
        if temp:
            user = UserModel.query.filter_by(Email=Email).first()
            if user:
                session['Forget_Email'] = Email
                return "您好。"
            else:
                return 'NONE'
        else:
            return 'Warning'


@bp.route("/forget_password3", methods=["POST"])
def forget_password3():
    if request.method == 'POST':
        try:
            Email = session.get('Forget_Email')
            password = request.form['password']
            temp = SQL_defend(password)
            if temp:
                user = UserModel.query.filter_by(Email=Email).first()
                user.Password = generate_password_hash(password)
                db.session.commit()
                return 'OK'
            else:
                return 'Warning'
        except KeyError:
            return 'CNM是不是有病'

@bp.route('/user_self/<string:Email>',methods=['GET','POST'])
@check_login
def user_self(Email):
    print(Email)
    if request.method=='GET':
        user=UserModel.query.filter_by(Email=Email).first()
        face_path={'face_path':user.Face_path}
        print(face_path)
        return render_template('user_self.html',**face_path)