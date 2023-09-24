from exts import db
from datetime import datetime


class UserModel(db.Model):
    __tablename__ = "user"
    ID = db.Column('ID',db.Integer,autoincrement=True,primary_key=True)
    Email = db.Column('Email', db.String(320), nullable=False)
    Username = db.Column('Username', db.String(20), unique=True)
    Password = db.Column('Password', db.String(120), nullable=False)
    join_time = db.Column('join_time', db.DateTime, default=datetime.now)
    Face_path = db.Column('Face_path', db.String(300),nullable=False)
