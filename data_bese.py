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
                    email VARCHAR(100) NOT NULL,
                    password VARCHAR(150)
                );
                '''
    cursor.executescript(table_script)
    connection.commit()
    connection.close()

def insert_user(username, email, password):
    connection, cursor = connect_to_db()
    cursor.execute("INSERT INTO User(username, email, password) VALUES(?, ?, ?)",
                   (username, email, password))
    connection.commit()
    connection.close()

def get_user_by_username(username):
    connection, cursor = connect_to_db()
    cursor.execute("SELECT id, username, email, password FROM User WHERE username = ?", [username])
    user = cursor.fetchone()
    connection.close()
    return user


def get_username_by_id(id):
    connection, cursor = connect_to_db()
    cursor.execute("SELECT username FROM User WHERE id = ?", [id])
    user_id = cursor.fetchone()[0]
    connection.close()
    return user_id


#notes table
def create_notes_table():
    connection, cursor = connect_to_db()
    table_script = '''CREATE TABLE IF NOT EXISTS Notes(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(50) NOT NULL,
                    encrypted TEXT NOT NULL,
                    note VARCHAR(250),
                    title VARCHAR(50),
                    public TEXT NOT NULL
                );
                '''
    cursor.executescript(table_script)
    connection.commit()
    connection.close()

def insert_note(username, note, encrypted, title, public):
    connection, cursor = connect_to_db()
    cursor.execute("INSERT INTO Notes(username, note, encrypted, title, public) VALUES(?, ?, ?, ?, ?)",
                   (username, note, encrypted, title, public))
    connection.commit()
    connection.close()

def get_notes_id_by_username(username):
    connection, cursor = connect_to_db()
    cursor.execute("SELECT id, title FROM Notes WHERE username = ?", [username])
    notes = cursor.fetchall()
    connection.close()
    return notes

def get_note_by_id(id):
    connection, cursor = connect_to_db()
    cursor.execute("SELECT username, encrypted, note, public FROM Notes WHERE id = ?", [id])
    note = cursor.fetchone()
    connection.close()
    return note

def delete_note_by_id(id):
    connection, cursor = connect_to_db()
    cursor.execute("DELETE FROM Notes WHERE id = ?", [id])
    cursor.execute("DELETE FROM SharedNotes WHERE note_id = ?", [id])
    connection.commit()
    connection.close()

def make_note_public(note_id):
    connection, cursor = connect_to_db()
    cursor.execute("UPDATE Notes SET public = 'true' WHERE id = ?", [note_id])
    connection.commit()
    connection.close()


#shared notes table
def create_sharedNotes_table():
    connection, cursor = connect_to_db()
    table_script = '''CREATE TABLE IF NOT EXISTS SharedNotes(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    by_user_id INTEGER NOT NULL,
                    to_user_id INTEGER NOT NULL,
                    note_id INTEGER NOT NULL,
                    FOREIGN KEY (by_user_id) REFERENCES User(id),
                    FOREIGN KEY (to_user_id) REFERENCES User(id),
                    FOREIGN KEY (note_id) REFERENCES Notes(id)
                );
                '''
    cursor.executescript(table_script)
    connection.commit()
    connection.close()

def get_shared_notes_id_by_username(username):
    connection, cursor = connect_to_db()
    to_user_id = get_user_by_username(username)[0]
    cursor.execute("SELECT note_id FROM SharedNotes WHERE to_user_id = ?", [to_user_id])
    notes = cursor.fetchall()
    connection.close()
    return notes

def get_shared_note_info_by_noteid(note_id):
    connection, cursor = connect_to_db()
    cursor.execute("SELECT by_user_id, to_user_id FROM SharedNotes WHERE note_id = ?", [note_id])
    notes = cursor.fetchone()
    connection.close()
    return notes

def insert_shared_note(shared_by_id, shared_to_id, note_id):
    connection, cursor = connect_to_db()
    cursor.execute("INSERT INTO SharedNotes(by_user_id, to_user_id, note_id) VALUES(?, ?, ?)",
                   (shared_by_id, shared_to_id, note_id))
    connection.commit()
    connection.close()