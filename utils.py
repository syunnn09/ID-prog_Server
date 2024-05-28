import json
from flask.wrappers import Request

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

def get_detail_data(user: int, _id: int) -> dict:
    for study in getStudies():
        if study['id'] == _id:
            return study
    return None

def replace_text(text: str) -> str:
    return text.replace('\n', '<br>').replace(' ', '&nbsp;').replace('\t', '&emsp;')

def check(request: Request):
    data: str = request.json['data']
    args: str = request.json['args']
    count = data.count('input()')
    count2 = args.count('\n') + 1
    return count == count2

if __name__ == '__main__':
    print(set_progress(1))
    # print(getStudies())
