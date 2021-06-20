import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file, check_same_thread=False)
    except Error as e:
        print(e)
    return conn
def create_table(conn):
    if conn is not None:
        try:
            sql = """ CREATE TABLE IF NOT EXISTS users (
                        id integer PRIMARY KEY AUTOINCREMENT,
                        uid text,
                        name text,
                        user_id text,
                        state text,
                        has_open_time_range text,
                        last_time_row text
                      ); """
            c = conn.cursor()
            c.execute(sql)
        except Error as e:
            print(e)
        try:
            sql = """ CREATE TABLE IF NOT EXISTS times (
                        id integer PRIMARY KEY AUTOINCREMENT,
                        user_uid text,
                        start_time text,
                        stop_time text,
                        sum_of_row text
                      ); """
            c = conn.cursor()
            c.execute(sql)
        except Error as e:
            print(e)
    else:
        print('Error: cannot connect to database')

def add_user(conn, uid, name, user_id, state, has_open_time_range = 0, last_time_row = 0):
    try:
        sql = ''' INSERT INTO users (uid, name, user_id, state, has_open_time_range, last_time_row)
                  VALUES(?,?,?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, (uid, name, user_id, state, has_open_time_range, last_time_row,))
        return cur.lastrowid
    except Error as e:
        print(e)
        return -1
def add_times(conn, user_uid, start_time, stop_time = '0', sum_of_row = '0'):
    try:
        sql = ''' INSERT INTO times (user_uid, start_time, stop_time, sum_of_row)
                  VALUES(?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, (user_uid, start_time, stop_time, sum_of_row,))
        return cur.lastrowid
    except Error as e:
        pritn('error in add_times()')
        print(e)
        return -1

def query_all_users(conn):
    try:
        cur = conn.cursor()
        cur.execute('SELECT uid, user_id FROM users')
        result = cur.fetchall()
        if result!=[]:
            return result
        else:
            return 0
    except Error as e:
        print(e)
        return 0
def query_user(conn, uid):
    try:
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE uid=?', (uid,))
        result = cur.fetchall()
        if result!=[]:
            return result[0]
        else:
            return 0
    except Error as e:
        print(e)
        return 'Fail'
def query_all_times(conn):
    try:
        cur = conn.cursor()
        cur.execute('SELECT * FROM times')
        result = cur.fetchall()
        if result!=[]:
            return result
        else:
            return 0
    except Error as e:
        print(e)
def query_user_times(conn, user_uid):
    try:
        cur = conn.cursor()
        cur.execute('SELECT start_time, stop_time, sum_of_row FROM times WHERE user_uid=?', (user_uid,))
        result = cur.fetchall()
        if result!=[]:
            return result
        else:
            return [0]
    except Error as e:
        print(e)
def query_time(conn, id):
    try:
        cur = conn.cursor()
        cur.execute('SELECT * FROM times WHERE id=?', (id,))
        result = cur.fetchall()
        if result!=[]:
            return result[0]
        else:
            return [0]
    except Error as e:
        pritn('error in query_time()')
        print(e)
def edit_times(conn, user_uid, start_time=None, stop_time=None, sum_of_row=None):
    if start_time!=None:
        try:
            cur = conn.cursor()
            cur.execute('UPDATE times SET start_time=? WHERE user_uid=?', (start_time, user_uid,))
            conn.commit()
        except Error as e:
            print(e)
    if stop_time!=None:
        try:
            cur = conn.cursor()
            cur.execute('UPDATE times SET stop_time=? WHERE user_uid=?', (stop_time, user_uid,))
            conn.commit()
        except Error as e:
            print(e)
    if sum_of_row!=None:
        try:
            cur = conn.cursor()
            cur.execute('UPDATE times SET sum_of_row=? WHERE user_uid=?', (sum_of_row, user_uid,))
            conn.commit()
        except Error as e:
            print(e)
def edit_times_byID(conn, row_number, user_uid, stop_time, sum_of_row):
    try:
        cur = conn.cursor()
        cur.execute('UPDATE times SET stop_time=?, sum_of_row=? WHERE user_uid=? AND id=?', (stop_time, sum_of_row, user_uid, row_number,))
        conn.commit()
    except Error as e:
        print(e)
def edit_user(conn, uid, name=None, user_id=None, state=None, has_open_time_range=None, last_time_row=None):
    if name!=None:
        try:
            cur = conn.cursor()
            cur.execute('UPDATE users SET name=? WHERE uid=?', (name, uid,))
            conn.commit()
        except Error as e:
            pritn('error in edit_user() in name')
            print(e)
    if user_id!=None:
        try:
            cur = conn.cursor()
            cur.execute('UPDATE users SET user_id=? WHERE uid=?', (user_id, uid,))
            conn.commit()
        except Error as e:
            pritn('error in edit_user() in user_id')
            print(e)
    if state!=None:
        try:
            cur = conn.cursor()
            cur.execute('UPDATE users SET state=? WHERE uid=?', (state, uid,))
            conn.commit()
        except Error as e:
            pritn('error in edit_user() in state')
            print(e)
    if has_open_time_range!=None:
        try:
            cur = conn.cursor()
            cur.execute('UPDATE users SET has_open_time_range=? WHERE uid=?', (has_open_time_range, uid,))
            conn.commit()
        except Error as e:
            pritn('error in edit_user() in has_open_time_range')
            print(e)
    if last_time_row!=None:
        try:
            cur = conn.cursor()
            cur.execute('UPDATE users SET last_time_row=? WHERE uid=?', (last_time_row, uid,))
            conn.commit()
        except Error as e:
            pritn('error in edit_user() in last_time_row')
            print(e)
