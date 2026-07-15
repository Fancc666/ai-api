# 测试蓝图
from flask import Blueprint, jsonify

bp = Blueprint('index', __name__, url_prefix='/api')

@bp.route('/')
def hello_api():
    return jsonify({
        "code": 0,
        "msg": "hello world",
        "data": None
    })
