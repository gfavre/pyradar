import sqlite3
from datetime import datetime


TABLE = "measures"
DB_PATH = 'radar.db'


def init_db(db_path=DB_PATH):
    con = sqlite3.connect(db_path)
    cursor = con.cursor()
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS "{TABLE}"
    (datetime TIMESTAMP NOT NULL, speed FLOAT NOT NULL, video_path VARCHAR NULL);
    """)
    con.commit()


def save_event(speed, video_path, db_path=DB_PATH):
    con = sqlite3.connect(db_path)
    cursor = con.cursor()
    sqlite_insert_with_param = f"""
    INSERT INTO '{TABLE}'
    ('datetime', 'speed', 'video_path')
    VALUES
    (?, ?, ?);
    """
    data_tuple = (datetime.now(), speed, str(video_path))
    cursor.execute(sqlite_insert_with_param, data_tuple)
    con.commit()
