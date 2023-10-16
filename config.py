from datetime import timedelta
from Global_config import sql_name,sql_password,sql_base,Mail,SECRET

class Config:
    # 配置参数
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{sql_name}:{sql_password}@127.0.0.1:3306/{sql_base}'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = "aohsnlklnakvavavno"
    # 邮箱配置
    # 项目中使用QQ邮箱
    MAIL_SERVER = "smtp.qq.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = Mail
    MAIL_PASSWORD = SECRET
    PERMANENT_SESSION_LIFETIME = timedelta(hours=0.1)
    FLASK_ADMIN_SWATCH='cerulean'
    BABEL_DEFAULT_LOCALE = "zh_CN"



