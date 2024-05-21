import json

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

if __name__ == '__main__':
    print(set_progress(1))
    # print(getStudies())
