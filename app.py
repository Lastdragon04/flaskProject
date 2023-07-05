import smtplib
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, session
from config import Config
from flask_migrate import Migrate
from exts import mail, System_name, db
from Model import UserModel
from Mail import Mail
from apps.user import bp as user_bp
from bll import create_captcha

app = Flask(__name__)
app.config.from_object(Config)
mail.init_app(app)
db.init_app(app)
migrate = Migrate(app, db)

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
        X = Mail().send_captcha(Register_Username, System_name, captcha, Register_Email)
        session['Register_Email_session'] = Register_Email[0]
        session['Register_Username'] = Register_Username
        session['captcha'] = captcha
    except smtplib.SMTPServerDisconnected:
        return 'Wrong'
    return 'OK'
