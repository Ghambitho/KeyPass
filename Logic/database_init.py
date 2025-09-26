import sqlite3
from pathlib import Path
import config

BASE = Path(__file__).resolve().parent.parent
DB_DIR = BASE / config.DB_PATH
DB_FILE = DB_DIR / config.DB_NAME

def init_database():
    try:
        DB_DIR.mkdir(exist_ok=True)
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS login (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                usuario TEXT UNIQUE NOT NULL,
                pass TEXT NOT NULL
            )
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS KEYPASS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                site TEXT NOT NULL,
                User TEXT NOT NULL,
                pass BLOB NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES login(id)
            )
        """)
        
        conn.commit()
        conn.close()
        
        return True
        
    except Exception:
        return False

