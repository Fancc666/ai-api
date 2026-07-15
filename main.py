from flask import Flask, request
from api import register_all
from utils.EnvironTool import config

app = Flask(__name__)
@app.after_request
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return resp
register_all(app)

def main():
    app.run(host='0.0.0.0', port=5520, debug=config.get('DEBUG', 'false').lower() == 'true')

if __name__ == "__main__":
    main()
