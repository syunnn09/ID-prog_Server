from flask import Flask, request, redirect
from flask_cors import CORS
from subprocess import TimeoutExpired
import subprocess
import json

import utils
import dbutils

app = Flask(__name__)
cors = CORS(app, resources={r'/*': {'origins': 'http://localhost:5173'}})

count = 0

def write(data):
    with open('data.py', 'w', encoding='utf-8') as f:
        f.write(data)

@app.route('/')
def index():
    return 'Hello'

@app.route('/question/solve', methods=['POST'])
def solve():
    try:
        uid = request.json['user']
        id = json.loads(request.json['id'])
        section = int(request.json['section'])
        question_no = int(request.json['question_no'])
    except Exception as e:
        print(f'{e = }')
        return {'status': 'false', 'reason': str(e)}

    try:
        dbutils.solve(uid, id, section, question_no)
    except Exception as e:
        print(f'{e = }')
        return {'status': 'false', 'reason': str(e)}
    return {'status': 'true'}


@app.route('/post', methods=['GET', 'POST'])
def post():
    write(request.json['data'])
    out = ''
    err = ''
    # utils.check(request)
    args: str = str(request.json['args'])
    try:
        p = subprocess.Popen('py data.py', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='shift-jis')
        out, err = p.communicate(timeout=5, input=args)
    except TimeoutExpired as e:
        p.kill()
        print(f'{e = }')
        err = str(e)
        err = err.replace('py data.py', 'main.py')
    except Exception as e:
        print(f'{e = }')
        err = e
    out = utils.replace_text(out)
    err = utils.replace_text(str(err))
    return {
        'res': out,
        'err': err
    }

@app.route('/login', methods=['POST'])
def login():
    global count
    count += 1
    return {
        "id": count,
        "ok": True
    }

@app.route('/api/data', methods=['POST'])
def get_data():
    uid = request.json['user']
    return json.dumps(utils.set_progress(uid))

@app.route('/api/getDetail', methods=['POST'])
def get_detail_data():
    if not utils.check_detail(request):
        return None
    _id = int(request.json['id'])
    uid = request.json['user']
    return json.dumps(utils.get_detail_data(uid, _id))

app.run('localhost', 55555, debug=False)
