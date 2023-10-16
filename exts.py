from flask_babel import Babel
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

mail = Mail()
admin=Admin()
db = SQLAlchemy()
babel=Babel()

