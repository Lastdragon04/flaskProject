import re

from exts import mail, Message
from Global_config import System_name


def send_captcha(register_username, captcha, register_email):
    sentence = """<div>
                        <h2>
                            您好:{}
                        </h2>   
                    </div>
                    <div>
                        <p>欢迎加入{}您的验证码为</p>
                            <div style="text-align: center;background: #062c33;color: white;font-size: x-large;width: 100vw;height: 20vh">
                                {}
                            </div>
                        <p>我们期待您的加入</p>
                        <p>请不要把该验证码发给其他人，以免造成不必要的安全或财产损失。如非本人操作请忽略此短信。</p>
                    </div>
                    """.format(register_username, System_name, captcha)
    msg = Message(subject=System_name, sender='1692930439@qq.com', recipients=register_email)
    msg.body = sentence
    mail.send(msg)
