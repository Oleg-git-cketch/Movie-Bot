import psycopg2
from psycopg2 import sql

DB_CONFIG = {
    "dbname": "moviebot",
    "user": "postgres",
    "password": "933780548LO",
    "host": "localhost",
    "port": "5432"
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def init_db():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS movies (
                    code TEXT PRIMARY KEY,
                    link TEXT,
                    image_id TEXT,   -- Новый столбец для фото
                    description TEXT -- Новый столбец для описания
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sponsors (
                    link TEXT PRIMARY KEY
                )
            """)
            conn.commit()

def add_movie_to_db(code, link, image_id, description):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute(
                    "INSERT INTO movies (code, link, image_id, description) VALUES (%s, %s, %s, %s)",
                    (code, link, image_id, description)
                )
                conn.commit()
                return True
            except psycopg2.IntegrityError:
                return False

def get_movie_by_code(code):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT link, image_id, description FROM movies WHERE code = %s", (code,))
            result = cursor.fetchone()
            return result if result else None

def update_movie_in_db(code, new_link, new_image_id, new_description):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE movies SET link = %s, image_id = %s, description = %s WHERE code = %s",
                (new_link, new_image_id, new_description, code)
            )
            conn.commit()
            return cursor.rowcount > 0

def delete_movie_from_db(code):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM movies WHERE code = %s", (code,))
            conn.commit()
            return cursor.rowcount > 0

def add_sponsor_to_db(link):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute("INSERT INTO sponsors (link) VALUES (%s)", (link,))
                conn.commit()
                return True
            except psycopg2.IntegrityError:
                return False

def get_all_sponsors():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT link FROM sponsors")
            return [row[0] for row in cursor.fetchall()]

def update_sponsor_in_db(old_link, new_link):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE sponsors SET link = %s WHERE link = %s", (new_link, old_link))
            conn.commit()
            return cursor.rowcount > 0

def delete_sponsor_from_db(link):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM sponsors WHERE link = %s", (link,))
            conn.commit()
            return cursor.rowcount > 0
