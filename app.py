from flask import Flask, request, redirect
from flask_cors import CORS
import subprocess

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
    write(request.json['data'])
    err = ''
    try:
        ret = subprocess.run("py data.py", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10, encoding="shift-jis")
    except Exception as e:
        print(e)
        err = e
    if ret.stderr:
        err = ret.stderr
    print(f'{ret.stderr = }')
    return {
        'res': ret.stdout,
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

app.run('localhost', 55555, debug=False)
