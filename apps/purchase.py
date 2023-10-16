from flask import Blueprint, request, session, jsonify, redirect, url_for,render_template
from check import check_login

bp = Blueprint('purchase', __name__, url_prefix='/purchase')

@bp.route('/index',methods=['GET'])
def purchase_index():
    if request.method=='GET':
        Information = {'Current_page': 'PURCHASE_INDEX'}
        return render_template('purchase.html',**Information)