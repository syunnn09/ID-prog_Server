-- CREATE TABLE users(
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     firebase_uid TEXT NOT NULL
-- );
-- DROP TABLE clear;

CREATE TABLE IF NOT EXISTS clear(
    increment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid TEXT NOT NULL,
    id INT NOT NULL,
    section INT NOT NULL,
    question_no INT NOT NULL,
    UNIQUE(uid, id, section, question_no)
);

CREATE TABLE IF NOT EXISTS questionnaire(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    good TEXT,
    bad TEXT
);
