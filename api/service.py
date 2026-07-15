from flask import Blueprint, jsonify, request
from pathlib import Path
from utils.AITool import AIHandler

def get_prompt(pt) -> Path:
    filePath = Path(__file__).parent.parent / 'prompts' / f'{pt}.md'
    return filePath
def get_glob() -> list:
    filePath = Path(__file__).parent.parent / 'prompts'
    globs = list(filePath.glob("*.md"))
    return list(map(lambda x: x.name, globs))
def get_data(file):
    with open(file, 'r') as f:
        return f.read()

bp = Blueprint('service', __name__, url_prefix='/api/service')

@bp.route('/')
def hello_api():
    return jsonify({
        "code": 1,
        "msg": "please select a service",
        "data": get_glob()
    })

@bp.route('/<string:serviceName>', methods=['GET', 'POST'])
def service_api(serviceName):
    ptFile = get_prompt(serviceName)
    if not ptFile.exists():
        return jsonify({
            "code": 1,
            "msg": f"service: {serviceName} not exist",
            "data": None
        })
    if request.method == 'GET':
        return jsonify({
            "code": 0,
            "msg": f"service: {serviceName} is running, use post method to send data",
            "data": None
        })
    # 检查用户输入
    userInput = request.form.get('input')
    if userInput is None:
        return jsonify({
            "code": 1,
            "msg": "no data sent for service",
            "data": None
        })
    # 调用AI功能
    promptText = get_data(ptFile)
    myai = AIHandler(promptText)
    try:
        response, _ = myai.send_request(userInput, [])
    except Exception as e:
        return jsonify({
        "code": 1,
        "msg": f"ai service error: {e}",
        "data": None
    })
    return jsonify({
        "code": 0,
        "msg": "success",
        "data": {
            "response": response
        }
    })
