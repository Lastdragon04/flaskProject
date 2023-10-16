from flask import session, redirect, url_for
from functools import wraps


def check_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 判断session是否保存了用户名，保存了即该用户已登录
        print('修饰器工作中')
        Email = session.get('Email')
        if Email:
            return func(*args, **kwargs)
        else:
            # 未登录重定向到登录页面
            print('未登录')
            return redirect(url_for('index'))
    return wrapper
