from flask import Flask,render_template,request
from flask_mail import Mail
from config import Config
from exts import mail
from apps.user import bp as user_bp


app=Flask(__name__)
app.config.from_object(Config)
mail.init_app(app)
app.register_blueprint(user_bp)

@app.route('/index',methods=['GET'])
def index():
    if request.method=='GET':
        return render_template('../templates/index.html')