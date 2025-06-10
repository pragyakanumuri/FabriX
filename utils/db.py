import sqlite3, os

DB = "fashion_app.db"

def init_db():
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        # store designs as PNG bytes + metadata
        cur.execute("""
        CREATE TABLE IF NOT EXISTS designs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            title TEXT,
            apparel_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            img BLOB
        )
        """)
        # simple forum posts
        cur.execute("""
        CREATE TABLE IF NOT EXISTS posts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            design_id INTEGER,
            caption TEXT,
            likes INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()