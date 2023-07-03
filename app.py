import smtplib

from flask import Flask, render_template, request, session
from flask_mail import Mail, Message
from config import Config
from exts import mail, System_name
from apps.user import bp as user_bp
from bll import create_captcha

app = Flask(__name__)
app.config.from_object(Config)
mail.init_app(app)
app.register_blueprint(user_bp)
app.jinja_env.variable_start_string = '(('
app.jinja_env.variable_end_string = '))'


@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')


@app.route('/send_captcha', methods=['POST'])
def send_captcha():
    captcha = create_captcha(6)
    Register_Email = request.form.getlist('Register_Email')
    Register_Username = request.form['Register_Username']
    try:
        sentence = """<div>
                        <h2>
                            您好:{}
                        </h2>   
                    </div>
                    <div>
                        <p>欢迎加入{}您的验证码为</p>
                            <div style="text-align: center;background: #062c33;color: white;font-size: x-large;width: 100vw;height: 20vh">
                                {}
                            </div>
                        <p>我们期待您的加入</p>
                        <p>请不要把该验证码发给其他人，以免造成不必要的安全或财产损失。如非本人操作请忽略此短信。</p>
                    </div>
                    """.format(request.form['Register_Username'], System_name, captcha)
        msg = Message(subject='艺源汽车服务中心管理系统', sender='1692930439@qq.com', recipients=Register_Email)
        msg.body = sentence
        mail.send(msg)
        session['Register_Email_session'] = Register_Email[0]
        session['Register_Username'] = Register_Username
        session['captcha'] = captcha
    except smtplib.SMTPServerDisconnected:
        return 'Wrong'
    return 'OK'
