import sqlite3

def init_db():
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movies (
        code TEXT PRIMARY KEY,
        link TEXT
    )
    """)
    conn.commit()
    conn.close()

def add_movie_to_db(code, link):
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO movies (code, link) VALUES (?, ?)", (code, link))
    conn.commit()
    conn.close()

def get_movie_by_code(code):
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()
    cursor.execute("SELECT link FROM movies WHERE code = ?", (code,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None
