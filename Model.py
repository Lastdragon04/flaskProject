from exts import db
from sqlalchemy import ForeignKey
from datetime import datetime


class UserModel(db.Model):
    __tablename__ = "user"
    ID = db.Column('ID', db.Integer, autoincrement=True, primary_key=True)
    Email = db.Column('Email', db.String(320), nullable=False)
    Username = db.Column('Username', db.String(20), unique=True)
    Password = db.Column('Password', db.String(120), nullable=False)
    join_time = db.Column('join_time', db.DateTime, default=datetime.now)
    Face_path = db.Column('Face_path', db.String(300), nullable=False)


class User_History(db.Model):
    __tablename__ = "history"
    H_ID = db.Column('H_ID', db.Integer, autoincrement=True, primary_key=True)
    U_ID = db.Column('U_ID', db.Integer, ForeignKey("user.ID", ondelete="CASCADE", onupdate="CASCADE"))
    Operation = db.Column('Operation', db.String(300), nullable=False)
    Time = db.Column('Time', db.DateTime, default=datetime.now)


class Raspberry(db.Model):
    __tablename__ = "Raspberry"
    R_ID = db.Column('R_ID', db.Integer, autoincrement=True, primary_key=True)
    owned = db.Column('owned', db.Integer, ForeignKey("user.ID", ondelete="CASCADE", onupdate="CASCADE"))
    Status = db.Column('Status', db.String(20), unique=True)
