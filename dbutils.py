import sqlite3

conn = sqlite3.connect('datab.db')
cur = conn.cursor()

sql = '''
CREATE TABLE sample(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT
);
'''

cur.execute(sql)

cur.close()
conn.commit()
conn.close()
