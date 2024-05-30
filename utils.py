import json
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

temp_progress = [15, 30, 75, 100]

def set_progress(user: int) -> list[dict]:
    ret = []
    for i, study in enumerate(getStudies()):
        item = study.copy()
        item['progress'] = temp_progress[i]
        ret.append(item)
    return ret

def add_clear_data(study: dict, clear_data: any) -> dict:
    ret = study.copy()
    for data in clear_data:
        section, question_no = data
        ret['sections'][section-1]['questions'][question_no-1]['isCleared'] = True
    return ret

def get_detail_data(user: int, _id: int) -> dict:
    clear_data = dbutils.get_clear(user, _id)
    for study in getStudies():
        if study['id'] == _id:
            return add_clear_data(study, clear_data)
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

def check_detail(request: Request):
    res = request.get_json('data') is not None
    res = res and request.get_json('user') is not None
    return res

def get_uid(user: str) -> str:
    user_obj = json.loads(user)
    return user_obj['uid']

if __name__ == '__main__':
    print(set_progress(1))
    # print(getStudies())
