import smtplib
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, session, g
from config import Config
from flask_migrate import Migrate
from exts import mail, db
from Global_config import System_name, System_logo,XiaoY
from apps.user import bp as user_bp
from Model import UserModel

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


@app.route('/about', methods=['GET'])
def about():
    if request.method == 'GET':
        return render_template('about_us.html')


@app.before_request
def before_request():
    user_email = session.get('Email')
    if user_email:
        user = UserModel.query.get(user_email)
        setattr(g, 'Email', user.Email)
    else:
        setattr(g, 'Email', None)


@app.context_processor
def my_context_processor():
    print('my_context_processor.g.Email', g.Email)
    return {"System_name": System_name, "School_logo": System_logo, 'Email': g.Email,
            'User_img': './static/img/User_default.jpg','XiaoY':XiaoY}
