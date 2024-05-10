from flask import Flask, request
from flask_cors import CORS
import subprocess

app = Flask(__name__)
cors = CORS(app, resources={r'/*': {'origins': 'http://localhost:5173'}})

def write(data):
    with open('data.py', 'w', encoding='utf-8') as f:
        f.write(data)

@app.route('/')
def index():
    return 'Hello'

@app.route('/post', methods=['GET', 'POST'])
def post():
    write(request.json['data'])
    try:
        ret = subprocess.run("py data.py", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10, encoding="utf-8")
    except subprocess.TimeoutExpired as e:
        print(e)
        return {
            'res': '',
            'err': e
        }
    print(f'{ret.stderr = }')
    return {
        'res': ret.stdout,
        'err': ret.stderr
    }

app.run('localhost', 55555, debug=False)
