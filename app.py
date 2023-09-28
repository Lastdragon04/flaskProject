import base64
import cv2
import numpy as np
from identify.start import face_detect_demo
from flask import Flask, render_template, request, session, g, redirect, url_for
import jinja2

from check import check_login
from config import Config
from flask_migrate import Migrate
from exts import mail, db,admin
from Global_config import System_name, get_System_logo, XiaoY
from apps.user import bp as user_bp
from Model import UserModel

from flask_socketio import SocketIO, send, emit
from flask_request_id import RequestID


import eventlet

eventlet.monkey_patch()

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config.from_object(Config)

admin.init_app(app)
mail.init_app(app)
socketio = SocketIO()
socketio.init_app(app, cors_allowed_origins='*')
db.init_app(app)

migrate = Migrate(app, db)
temp_request = RequestID(app)

app.register_blueprint(user_bp)



@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')


@app.route('/docs', methods=['GET'])
@check_login
def docs():
    if request.method == 'GET':
        return render_template('index.html')


@app.before_request
def before_request():
    Email = session.get('Email')
    Username = session.get('Username')
    if Email and Username:
        user = UserModel.query.filter_by(Email=Email,Username=Username).first()
        user.Status='Login'
        db.session.commit()
        setattr(g, 'Email', user.Email)
        setattr(g, 'Username', user.Username)
    else:
        setattr(g, 'Email', None)
        setattr(g, 'Username', None)


@app.context_processor
def my_context_processor():
    print('当前登录的用户为', g.Email)
    return {"System_name": System_name, "School_logo": get_System_logo(), 'Email': g.Email,
            'User_img': './static/img/User_default.jpg', 'XiaoY': XiaoY, 'Username': g.Username}


@app.route('/select', methods=['GET'])
def select():
    user = []
    List = UserModel.query.all()
    for i in List:
        templist = []
        templist.append(i.Username)
        templist.append(i.Email)
        user.append(templist)
    print(user)
    return 'OKK'


@socketio.on('connect')
def handle_connect():
    session[temp_request.id] = 0
    print("客户端已连接")


@socketio.on('video_frame1')
def handle_video_frame(data):
    try:
        user = []
        Forget_Emial = session.get('Forget_Email')
        List = UserModel.query.all()
        for i in List:
            user.append(i.Email)
        # print(user)
        # 将bs4转成原始字节
        encoded_data = data.split(",")[1]
        nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)

        # # 人脸识别部分
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        Email = face_detect_demo(image, Email_list=user)
        print(Email)
        temp_id = temp_request.id
        count = session.get(temp_id)
        print('识别出的用户名', Email)
        if Email == Forget_Emial:
            if count < 0:
                count = 0
            session.pop(temp_id)
            session[temp_id] = count + 1
            print('成功一次')
            print('当前分数:', count)
            if count >= 50:
                return 'success'
        else:
            session.pop(temp_id)
            session[temp_id] = count - 2
            print('失败一次')
            print('当前分数:', count)
        return count
    except KeyError:
        return -50


@socketio.on('disconnect')
def handle_disconnect():
    session.pop('Forget_Email')
    print("客户端已断开")


@app.before_request
def log_each_request():
    app.logger.info('method:{},path:{},ip:{},user:{}'.format(request.method, request.path, request.remote_addr,session.get('Email')))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
    socketio.run(app)
