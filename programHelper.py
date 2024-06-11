import utils
import subprocess

from subprocess import TimeoutExpired
from flask import request

def write(data):
    with open('data.py', 'w', encoding='utf-8') as f:
        f.write(data)

def execute(data: str, args: str) -> dict[str, str]:
    write(data)
    out = ''
    err = ''
    args: str = str(args)
    try:
        p = subprocess.Popen('py data.py', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='shift-jis')
        out, err = p.communicate(timeout=5, input=args)
    except TimeoutExpired as e:
        p.kill()
        print(f'{e = }')
        err = e
    except Exception as e:
        print(f'{e = }')
        err = e
    out = utils.replace_text(out)
    err = utils.replace_text(str(err))
    return {
        'res': out,
        'err': err
    }
