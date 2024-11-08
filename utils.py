import math
import json
from typing import Any
from flask.wrappers import Request

import dbutils

with open('./studyData.json', 'r', encoding='utf-8') as f:
    data = json.loads(f.read())

studyTitles = None

def getStudies() -> list[dict]:
    global studyTitles

    # if studyTitles is None:
    with open('./studyData.json', 'r', encoding='utf-8') as f:
        data = json.loads(f.read())
    studyTitles = [study for study in data['studies']]

    return studyTitles.copy()

def get_total_questions() -> list[int]:
    questions = []
    for i, study in enumerate(data['studies']):
        questions.append(0)
        for section in study['sections'][1:]:
            questions[i] += len(section['questions'])
    return questions

def parse_clear_data(clear_data: list[tuple[int]], studies) -> list[int]:
    questions = [0 for _ in range(studies)]
    for clear in clear_data:
        _id, _, _ = clear
        questions[_id-1] += 1
    return questions

def get_progress(user: str) -> list[int]:
    questions = get_total_questions()
    clear_data = dbutils.get_all_clear(user)
    clears = parse_clear_data(clear_data, len(questions))
    progress = []
    for question, clear in zip(questions, clears):
        progress.append(math.floor((clear / question) * 100))
    return progress

def set_progress(user: str) -> list[dict]:
    ret = []
    progress = get_progress(user)
    for i, study in enumerate(getStudies()):
        study['progress'] = progress[i]
        ret.append(study)
    return ret


def add_clear_data(study: dict, clear_data: Any) -> dict:
    for section in study['sections']:
        questions = len(section['questions'])
        clears = len(list(filter(lambda x: x[0] == section['section'], clear_data)))
        if questions:
            study['sections'][section['section']-1]['progress'] = math.floor((clears / questions) * 100)
        else:
            study['sections'][section['section']-1]['progress'] = 0

    return study

def get_study(url: str) -> dict:
    for study in getStudies():
        if study['url'] == url:
            return study.copy()
    return None

def get_detail_data(user: int, url: str) -> dict:
    study = get_study(url)
    if study is None:
        return None
    clear_data = dbutils.get_clear(user, study['id'])
    return add_clear_data(study, clear_data)

def add_sample_data(ret: dict) -> dict:
    for question in ret['questions']:
        question['examples'] = []
        for test in question['tests'][:2]:
            test['input'] = test['input'].replace('\n', '<br>')
            test['output'] = test['output'].replace('\n', '<br>')
            question['examples'].append(test)
    return ret

def add_section_data(study: dict, clear_data: Any, id: int) -> dict:
    for data in clear_data:
        study['id'] = id
        study['questions'][data[0]-1]['isCleared'] = True
    if study['title'] == '確認問題':
        study = add_sample_data(study)
    return study

def get_section_data(uid: str, url: str, section: int) -> dict:
    study = get_study(url)
    if study is None:
        return None
    for s in study['sections']:
        if s['section'] == section:
            clear_data = dbutils.get_section_clear(uid, study['id'], section)
            return add_section_data(s, clear_data, study['id'])
    return None

def replace_text(text: str) -> str:
    return text \
            .replace(' ', '&nbsp;') \
            .replace('\t', '&emsp;') \
            .replace('<', '&lt;') \
            .replace('>', '&gt;') \
            .replace('\n', '<br>')


def check(request: Request):
    data: str = request.json['data']
    args: str = request.json['args']
    count = data.count('input(')
    if count:
        count2 = args.count('\n') + 1
        return count == count2
    return True


def check_detail(request: Request) -> bool:
    res = request.get_json('url') is not None
    res = res and request.get_json('user') is not None
    return res

def check_section(request: Request) -> bool:
    res = request.get_json('url') is not None
    res = res and request.get_json('section') is not None
    res = res and request.get_json('user') is not None
    return res

def get_section(study: dict, section: int) -> dict:
    for s in study['sections']:
        if s['section'] == section:
            return s
    return None

def get_question(section: dict, question_no: int) -> dict:
    for question in section['questions']:
        if question['question_no'] == question_no:
            return question
    return None

def get_args(request: Request) -> str:
    url = request.json['url']
    section = int(request.json['section'])
    question_no = request.json['question_no']
    test_no = int(request.json['test_no'])
    study = get_study(url)
    section = get_section(study, section)
    question = get_question(section, question_no)
    return question['tests'][test_no]

errors = {
    SyntaxError: {
        'string': "SyntaxError",
        'text': ': や ) などが抜けている可能性があります',
    },
    IndentationError: {
        'string': 'IndentationError',
        'text': 'インデントが抜けている可能性があります',
    },
    NameError: {
        'string': 'NameError',
        'text': '宣言されていない変数が参照されました',
    },
    TypeError: {
        'string': 'TypeError',
        'text': '異なるデータ型の演算が行われました',
    },
    ValueError: {
        'string': 'ValueError',
        'text': '関数に不適切な値が渡されました',
    },
    AttributeError: {
        'string': 'AttributeError',
        'text': '「型」型に「属性」という属性は存在しません',
    },
    IndexError: {
        'string': 'IndexError',
        'text': 'リストの要素外を参照しました',
    },
    KeyError: {
        'string': 'KeyError',
        'text': '存在しない辞書のキーを指定しました',
    },
    ModuleNotFoundError: {
        'string': 'ModuleNotFoundError',
        'text': '存在しないモジュールをインポートしました',
    },
    ZeroDivisionError: {
        'string': 'ZeroDivisionError',
        'text': '0で割り算が行われました'
    },
}

def raise_error(err: str):
    for error, v in errors.items():
        string = v.get('string')
        text = v.get('text')
        if string in err:
            raise error(text)

if __name__ == '__main__':
    print(get_progress('cJ2HzFoEExXyHZr7yzQMWv0OOHe2'))
    # print(getStudies())
