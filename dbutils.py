import sqlite3
import threading

conn = sqlite3.connect('data.db', check_same_thread=False)
cur = conn.cursor()

lock = threading.Lock()

def solve(uid: str, id: int, section: int, question_no: int) -> None:
    try:
        sql = 'INSERT INTO clear(uid, id, section, question_no) VALUES(?, ?, ?, ?)'
        cur.execute(sql, (uid, id, section, question_no, ))
        conn.commit()
    except Exception as e:
        raise Exception(e)

def get_clear(user: str, id: int) -> list[tuple[int]]:
    sql = 'SELECT section, question_no FROM clear WHERE uid=? AND id=?'
    cur.execute(sql, (user, id, ))
    return cur.fetchall()

def get_all_clear(user: str) -> list[tuple[int]]:
    try:
        lock.acquire(True)
        sql = 'SELECT id, section, question_no FROM clear WHERE uid=?'
        cur.execute(sql, (user, ))
    finally:
        lock.release()
    return cur.fetchall()

def get_clear_by_section(user: str, section: int) -> list[tuple[int]]:
    sql = 'SELECT id, section, question_no FROM clear WHERE uid=? AND section=?'
    cur.execute(sql, (user, section, ))
    return cur.fetchall()

def get_section_clear(user: str, id: int, section: int) -> list[tuple[int]]:
    sql = 'SELECT question_no FROM clear WHERE uid=? AND id=? AND section=?'
    cur.execute(sql, (user, id, section))
    return cur.fetchall()


def update_section():
    # cur.execute('UPDATE clear SET section = section + 1 WHERE id=4')
    cur.execute('DELETE FROM clear WHERE section=1')
    # cur.execute('DELETE FROM clear')
    conn.commit()
    cur.close()
    conn.close()

def questionnaire(good: str, bad: str):
    sql = 'INSERT INTO questionnaire(good, bad) VALUES(?, ?)'
    cur.execute(sql, (good, bad, ))
    conn.commit()

def get_questionnaire():
    sql = 'SELECT * FROM questionnaire'
    cur.execute(sql)
    return cur.fetchall()

if __name__ == '__main__':
    update_section()
