import re

from exts import mail, Message


def SQL_defend(SQL_sentence):
    pattern = re.compile(
        r"(%27)|(\')|(\-\-)|(%23)|(#)|"  # Regex for detection of SQL meta-characters
        r"\w*((%27)|(\'))\s+((%6F)|o|(%4F))((%72)|r|(%52))\s*|"  # Modified regex for detection of SQL meta-characters eg: ' or 1 = 1' detect word 'or',
        r"((%3D)|(=))[^\n]*((%27)|(\')|(\-\-)|(%3B)|(;))"  # Regex for typical SQL Injection attack eg: '= 1 --'
        r"((%27)|(\'))union|"  # Regex for detecting SQL Injection with the UNION keyword
        r"((%27)|(\'))select|"  # Regex for detecting SQL Injection with the UNION keyword
        r"((%27)|(\'))insert|"  # Regex for detecting SQL Injection with the UNION keyword
        r"((%27)|(\'))update|"  # Regex for detecting SQL Injection with the UNION keyword
        r"((%27)|(\'))drop",  # Regex for detecting SQL Injection with the UNION keyword
        re.IGNORECASE,
    )
    r = pattern.search(SQL_sentence)
    if r:
        return False
    else:
        return True


def send_captcha(register_username, system_name, captcha, register_email):
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
                    """.format(register_username, system_name, captcha)
    msg = Message(subject='艺源汽车服务中心管理系统', sender='1692930439@qq.com', recipients=register_email)
    msg.body = sentence
    mail.send(msg)
