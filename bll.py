from string import ascii_letters, digits
from random import sample


def create_captcha(number):
    letters = ascii_letters + digits
    captcha = "".join(sample(letters, number))
    return captcha

