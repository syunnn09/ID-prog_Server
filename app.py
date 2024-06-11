from flask import Flask, request, redirect
from flask_cors import CORS
from subprocess import TimeoutExpired
import subprocess
import json

import utils
import dbutils
import programHelper

app = Flask(__name__)
cors = CORS(app, resources={r'/*': {'origins': 'http://localhost:5173'}})

count = 0

@app.route('/')
def index():
    return 'Hello'

@app.route('/question/solve', methods=['POST'])
def solve():
    try:
        uid = request.json['user']
        id = int(request.json['id'])
        section = int(request.json['section'])
        question_no = int(request.json['question_no'])
    except Exception as e:
        print(f'1: {e = }')
        return {'status': False, 'reason': str(e)}

    try:
        dbutils.solve(uid, id, section, question_no)
    except Exception as e:
        print(f'2: {e = }')
        return {'status': False, 'reason': str(e)}
    return {'status': True}


@app.route('/post', methods=['POST'])
def post():
    data = request.json['data']
    args = request.json['args']
    return programHelper.execute(data, args)

@app.route('/test', methods=['POST'])
def test():
    data = request.json['data']
    args = utils.get_args(request)
    result = programHelper.execute(data, args['input'].replace('<br>', '\n'))
    result['correct'] = result['res'] == args['output']
    return result

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
    url = request.json['url']
    uid = request.json['user']
    return json.dumps(utils.get_detail_data(uid, url))

@app.route('/api/getSection', methods=['POST'])
def get_section_data():
    if not utils.check_section(request):
        return None
    section = int(request.json['section'])
    url = request.json['url']
    uid = request.json['user']

    return json.dumps(utils.get_section_data(uid, url, section))

app.run('localhost', 55555, debug=False)
