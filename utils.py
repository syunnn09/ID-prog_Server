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

    if studyTitles is None:
        studyTitles = [study for study in data['studies']]

    return studyTitles

def get_total_questions() -> list[int]:
    questions = []
    for i, study in enumerate(data['studies']):
        questions.append(0)
        for section in study['sections']:
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
        item = study.copy()
        item['progress'] = progress[i]
        ret.append(item)
    return ret


def add_clear_data(study: dict, clear_data: Any) -> dict:
    ret = study.copy()
    for data in clear_data:
        section, question_no = data
        ret['sections'][section-1]['questions'][question_no-1]['isCleared'] = True
    return ret

def get_study(url: str):
    for study in getStudies():
        if study['url'] == url:
            return study
    return None

def get_detail_data(user: int, url: str) -> dict:
    study = get_study(url)
    if study is None:
        return None
    clear_data = dbutils.get_clear(user, study['id'])
    return add_clear_data(study, clear_data)

def add_section_data(study: dict, clear_data: Any) -> dict:
    ret = study.copy()
    print(clear_data)
    for data in clear_data:
        ret['questions'][data[0]-1]['isCleared'] = True
    return ret

def get_section_data(uid: str, url: str, section: int):
    study = get_study(url)
    if study is None:
        return None
    for s in study['sections']:
        if s['section'] == section:
            clear_data = dbutils.get_section_clear(uid, study['id'], section)
            return add_section_data(s, clear_data)
    return None

def replace_text(text: str) -> str:
    return text.replace('\n', '<br>').replace(' ', '&nbsp;').replace('\t', '&emsp;')


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

if __name__ == '__main__':
    print(get_progress('cJ2HzFoEExXyHZr7yzQMWv0OOHe2'))
    # print(getStudies())
