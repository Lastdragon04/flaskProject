from flask import Flask, render_template, request
from flask_mail import Mail
from config import Config
from exts import mail
from apps.user import bp as user_bp

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
