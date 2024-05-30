import sqlite3

conn = sqlite3.connect('data.db', check_same_thread=False)
cur = conn.cursor()

def solve(uid: str, id: int, section: int, question_no: int):
    try:
        sql = 'INSERT INTO clear(uid, id, section, question_no) VALUES(?, ?, ?, ?)'
        cur.execute(sql, (uid, id, section, question_no, ))
        conn.commit()
    except Exception as e:
        raise Exception(e)

def get_clear(user: str, id: int):
    sql = 'SELECT section, question_no FROM clear WHERE uid=? AND id=?'
    cur.execute(sql, (user, id, ))
    return cur.fetchall()
