import sqlite3
from datetime import datetime

DB_PATH = "chordeley.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
                CREATE TABLE IF NOT EXISTS progressions(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title      TEXT NOT NULL,
                chords     TEXT NOT NULL,
                key_root   TEXT,
                memo       TEXT,
                tags       TEXT,
                created_at TEXT NOT NULL
                )   
    """)
    conn.commit()
    conn.close()

def add_progression(Title,chords,key_root,memo,tags):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """INSERT INTO progressions
        (title, chords, key_root, memo, tags, created_at)
        VALUES(?,?,?,?,?,?)""",
         (Title, chords, key_root, memo, tags,
         datetime.now().strftime("%Y-%m-%d %H:%M"))
    )
    conn.commit()
    conn.close()

def get_all_progressions():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    progressions = conn.execute(
        """SELECT id, title, chords, key_root, memo, tags, created_at
        FROM progressions
        ORDER BY id DESC"""
    ).fetchall()
    conn.close()
    return progressions

def delete_progression(progression_id):
    # 指定したIDのデータを削除する
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "DELETE FROM progressions WHERE id = ?", (progression_id,)
    )
    conn.commit()
    conn.close()
