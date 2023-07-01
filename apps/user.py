from flask import Blueprint, render_template

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/register1', methods=['POST'])
def register1():
    return
