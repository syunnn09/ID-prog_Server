from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r'/*': {'origins': 'http://localhost:5173'}})

@app.route('/')
def index():
    return 'Hello'

@app.route('/post', methods=['GET', 'POST'])
def post():
    print(request.get_data())
    return 'ok'

app.run('localhost', 55555, debug=True)
