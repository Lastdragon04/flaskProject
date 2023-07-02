from flask import Flask, render_template, request
from flask_mail import Mail, Message
from config import Config
from exts import mail
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
    print(Register_Email)
    sentence = '您在艺源汽车服务中心管理系统注册的验证码为%s' % captcha
    msg = Message(subject='艺源汽车服务中心管理系统', sender='1692930439@qq.com', recipients=Register_Email)
    msg.body = sentence
    mail.send(msg)
    return 'OK'
