from datetime import timedelta


class Config:
    # 配置参数
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123654@127.0.0.1:3306/reptile_sys'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = "aohsnlklnakvavavno"
    # 邮箱配置
    # 项目中使用QQ邮箱
    MAIL_SERVER = "smtp.qq.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = '1692930439@qq.com'
    MAIL_PASSWORD = 'unhsvhulyrvaeeei'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
