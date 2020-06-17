import sqlite3
from sqlite3 import Error
conn = None
def create_connection(db_file, script):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        with open(script, 'r') as file:
            query=file.read()
        c = conn.cursor()
        c.executescript(query)
        conn.commit()
        c.close()
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
def runscript(db_file, script):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        with open(script, 'r') as file:
            query=file.read()
        c = conn.cursor()
        c.executescript(query)
        conn.commit()
        c.close()
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def getConnection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
if __name__ == '__main__':
    create_connection(r"bible_jw.db", r"bible_jw.sql")
    runscript(r"bible_jw.db", r"en_bible_data.sql")
    #getConnection(r"bible_jw.db")