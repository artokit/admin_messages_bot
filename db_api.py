import sqlite3
from sqlite3 import IntegrityError

connect = sqlite3.connect('db.sqlite')
cursor = connect.cursor()
cursor.execute("DELETE FROM USERS WHERE user_id = 5833820044")
connect.commit()


def add_user(user_id: int) -> bool:
    try:
        cursor.execute("INSERT INTO USERS VALUES(?, null)", (user_id, ))
        connect.commit()
        return True
    except IntegrityError:
        return False


def set_thread_id(user_id: int, thread_id: int):
    if not get_user(user_id)[1]:
        cursor.execute("UPDATE USERS SET thread_id = ? WHERE USER_ID = ?", (thread_id, user_id))
        connect.commit()


def get_user(user_id: int):
    return cursor.execute('SELECT * FROM USERS where user_id = ?', (user_id, )).fetchone()


def get_user_by_thread_id(thread_id: int):
    return cursor.execute('SELECT * FROM USERS WHERE thread_id = ?', (thread_id, )).fetchone()
