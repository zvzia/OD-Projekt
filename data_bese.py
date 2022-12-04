from sqlite3 import connect
from sqlite3.dbapi2 import Cursor

DB_NAME = "notes_app.db"  

def connect_to_db():
    connection = connect(DB_NAME)
    cursor = connection.cursor()
    return connection, cursor

#user table
def create_user_table():
    connection, cursor = connect_to_db()
    table_script = '''CREATE TABLE IF NOT EXISTS User(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(50) NOT NULL UNIQUE,
                    password VARCHAR(150)
                );
                '''
    cursor.executescript(table_script)
    connection.commit()
    connection.close()

def insert_user(username, password):
    connection, cursor = connect_to_db()
    cursor.execute("INSERT INTO User(username, password) VALUES(?, ?)",
                   (username, password))
    connection.commit()
    connection.close()

def get_user_by_username(username):
    connection, cursor = connect_to_db()
    cursor.execute("SELECT * FROM User WHERE username = ?", [username])
    user = cursor.fetchone()
    connection.close()
    return user


#notes table
def create_notes_table():
    connection, cursor = connect_to_db()
    table_script = '''CREATE TABLE IF NOT EXISTS Notes(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(50) NOT NULL UNIQUE,
                    note VARCHAR(250)
                );
                '''
    cursor.executescript(table_script)
    connection.commit()
    connection.close()

def insert_note(username, note):
    connection, cursor = connect_to_db()
    cursor.execute("INSERT INTO Notes(username, note) VALUES(?, ?)",
                   (username, note))
    connection.commit()
    connection.close()

def get_notes_id_by_username(username):
    connection, cursor = connect_to_db()
    cursor.execute("SELECT id FROM Notes WHERE username = ?", [username])
    notes = cursor.fetchall()
    connection.close()
    return notes

def get_note_by_id(id):
    connection, cursor = connect_to_db()
    cursor.execute("SELECT username, note FROM Notes WHERE id = ?", [id])
    note = cursor.fetchone()
    connection.close()
    return note