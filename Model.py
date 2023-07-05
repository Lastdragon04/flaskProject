from exts import db
from datetime import datetime


class UserModel(db.Model):
    __tablename__ = "user"
    Email = db.Column('Email', db.String(320), primary_key=True)
    Username = db.Column('Username', db.String(20), nullable=False)
    join_time = db.Column('join_time', db.DateTime, default=datetime.now)
