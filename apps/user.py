from flask import Blueprint, render_template, request, session,redirect,url_for
from smtplib import SMTPServerDisconnected
from werkzeug.security import generate_password_hash, check_password_hash
from bll import create_captcha
from exts import db
from Mail import send_captcha
from SQL_Defence import SQL_defend
from Model import UserModel
from Global_config import System_name

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/register1_send_captcha', methods=['POST'])
def register1():
    captcha = create_captcha(6)
    Register_Email = request.form.getlist('Register_Email')
    Register_Username = request.form['Register_Username']
    try:
        X = send_captcha(Register_Username, System_name, captcha, Register_Email)
        session['Register_Email_session'] = Register_Email[0]
        session['Register_Username'] = Register_Username
        session['captcha'] = captcha
    except SMTPServerDisconnected:
        return 'Wrong'
    return 'OK'


@bp.route("/register2_get_captcha", methods=['POST'])
def register2_get_captcha():
    if request.method == 'POST':
        captcha = request.form['captcha']
        try:
            server_captcha = session.get('captcha')
            session.pop('captcha')
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
            Username = session['Register_Username']
            Email = session.get('Register_Email_session')
            password = request.form['password']
            session.pop('Register_Username')
            session.pop('Register_Email_session')
            print(Username, Email, password)
            user = UserModel(Email=Email, Username=Username, Password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return 'OK'
        except KeyError:
            return '我真草泥马，老子小网站你攻击你妈攻击,他妈学了地点爬虫就给你牛逼死了哈，回去好好再学学你那javascript，有种来攻击老子服务器'


@bp.route("/login", methods=['POST'])
def Login():
    if request.method == 'POST':
        Password = request.form['Password']
        Email = request.form['Email']
        Email_Defence = SQL_defend(Password)
        if Email_Defence:
            user = UserModel.query.filter_by(Email=Email).first()
            print(user)
            if not user:
                return 'None'
            else:
                if check_password_hash(user.Password, Password):
                    session['Email'] = Email
                    return 'OK'
                else:
                    return 'Error'
        else:
            return 'Wrong'
