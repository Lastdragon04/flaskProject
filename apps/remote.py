from flask import Blueprint, request,render_template

bp = Blueprint('control', __name__, url_prefix='/control')


@bp.route('link_raspiberry', methods=['POST', 'GET'])
def link_raspiberry():
    if request.method == 'POST':
        return 'OK'


@bp.route('/index')
def remote():
    Information = {'Current_page': 'CONTROL_INDEX'}
    return render_template('Control.html',**Information)
