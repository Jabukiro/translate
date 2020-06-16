import sqlite3
from sqlite3 import Error
def create_connection(db_file, script):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        with open(script, 'r') as file:
            query=file.read()
        c = conn.cursor()
        c.executescript(query)
        c.close()
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    create_connection(r"bible_jw.db", r"bible_jw.sql")