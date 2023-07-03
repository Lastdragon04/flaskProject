from flask import Blueprint, render_template, request, session

bp = Blueprint('user', __name__, url_prefix='/user')


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


@bp.route("/register3",methods=['POST'])
def register3():
    if request.method=='POST':
        Username=session['Register_Username']
        Email=session.get('Register_Email_session')
        password=request.form['password']
        print(Username,Email,password)
        return 'OK'

