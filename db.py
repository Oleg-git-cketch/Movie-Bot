import sqlite3

db_path = "database.db"

def get_connection():
    return sqlite3.connect(db_path)


def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()

        # Создание таблицы movies
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                code TEXT PRIMARY KEY,
                link TEXT,
                image_id TEXT,
                description TEXT
            )
        """)

        # Создание таблицы sponsors
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sponsors (
                link TEXT PRIMARY KEY,
                is_mandatory INTEGER DEFAULT 1
            )
        """)
        conn.commit()


def add_movie_to_db(code, link, image_id, description):
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO movies (code, link, image_id, description) VALUES (?, ?, ?, ?)",
                (code, link, image_id, description)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

def get_movie_by_code(code):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT link, image_id, description FROM movies WHERE code = ?", (code,))
        result = cursor.fetchone()
        return result if result else None

def update_movie_in_db(code, new_link, new_image_id, new_description):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE movies SET link = ?, image_id = ?, description = ? WHERE code = ?",
            (new_link, new_image_id, new_description, code)
        )
        conn.commit()
        return cursor.rowcount > 0

def delete_movie_from_db(code):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM movies WHERE code = ?", (code,))
        conn.commit()
        return cursor.rowcount > 0

def add_sponsor_to_db(link, is_mandatory=1):
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO sponsors (link, is_mandatory) VALUES (?, ?)", (link, is_mandatory))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

def get_all_sponsors():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT link, is_mandatory FROM sponsors")
        return cursor.fetchall()  # Теперь возвращаем кортеж (ссылка, обязательность)

def update_sponsor_in_db(old_link, new_link, is_mandatory):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE sponsors SET link = ?, is_mandatory = ? WHERE link = ?", (new_link, is_mandatory, old_link))
        conn.commit()
        return cursor.rowcount > 0

def delete_sponsor_from_db(link):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sponsors WHERE link = ?", (link,))
        conn.commit()
        return cursor.rowcount > 0