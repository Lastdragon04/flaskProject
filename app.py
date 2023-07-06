import smtplib
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, session
from config import Config
from flask_migrate import Migrate
from exts import mail, System_name, db

from apps.user import bp as user_bp

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


@app.context_processor
def my_context_processor():
    return {"System_name": System_name}


