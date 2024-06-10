import sqlite3

conn = sqlite3.connect('data.db', check_same_thread=False)
cur = conn.cursor()

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
    sql = 'SELECT id, section, question_no FROM clear WHERE uid=?'
    cur.execute(sql, (user, ))
    return cur.fetchall()

def get_clear_by_section(user: str, section: int) -> list[tuple[int]]:
    sql = 'SELECT id, section, question_no FROM clear WHERE uid=? AND section=?'
    cur.execute(sql, (user, section, ))
    return cur.fetchall()

def get_section_clear(user: str, id: int, section: int) -> list[tuple[int]]:
    sql = 'SELECT question_no FROM clear WHERE uid=? AND id=? AND section=?'
    cur.execute(sql, (user, id, section))
    return cur.fetchall()
