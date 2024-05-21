from flask import Flask, request, redirect
from flask_cors import CORS
import subprocess
import json

import utils

app = Flask(__name__)
cors = CORS(app, resources={r'/*': {'origins': 'http://localhost:5173'}})

count = 0

def write(data):
    with open('data.py', 'w', encoding='shift-jis') as f:
        f.write(data)

@app.route('/')
def index():
    return 'Hello'

@app.route('/redirect')
def red():
    return redirect('/')

@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.json['user']:
        with open('user.json', 'w') as f:
            f.write(json.dumps(request.json['user'], indent=4))
    write(request.json['data'])
    out = ''
    err = ''
    try:
        ret = subprocess.run("py data.py", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5, encoding="shift-jis")
        out = ret.stdout
        if ret.stderr:
            err = ret.stderr
    except Exception as e:
        print(f'{e = }')
        err = e
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

@app.route('/api/data')
def get_data():
    print(request.get_data('user'))
    return json.dumps(utils.set_progress(1))

app.run('localhost', 55555, debug=False)
