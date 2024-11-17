import sqlite3

def get_connection():
    try:
        con = sqlite3.connect('journal.db')
        con.row_factory = sqlite3.Row
        print("Успешное подключение!")
        return con
    except Exception:
        print("Ошибка подключения!")


def users():
    con = get_connection()
    with con:
        c = con.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS Users
    (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT NOT NULL,
    psw TEXT NOT NULL,
    UNIQUE ("login") ON CONFLICT IGNORE
    );
    ''')
    con.commit()


def dates():
    con = get_connection()
    with con:
        c = con.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS Dates
(
id INTEGER PRIMARY KEY AUTOINCREMENT,
date TEXT NOT NULL
);
    ''')
    con.commit()


def journals():
    con = get_connection()
    with con:
        c = con.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS Journals
(
id INTEGER PRIMARY KEY AUTOINCREMENT,
diary TEXT,
dates_id INTEGER,
users_id INTEGER,
FOREIGN KEY (dates_id) REFERENCES Dates(id),
FOREIGN KEY (users_id) REFERENCES Users(id)
);
    ''')
    con.commit()

def users_insert(login,psw):
    try:
        con= get_connection()
        with con:
            c = con.cursor()
        c.execute('''
                  INSERT INTO Users (login,psw) values
                  (?,?);
                  ''',(login,psw,))
        con.commit()
    except sqlite3.Error as error:
        print('Ошибка при работе sql', error)
    finally:
        if con:
            con.close()
            print('Соединение с sql закрыто')

def dates_insert(dates):
    try:
        con= get_connection()
        with con:
            c = con.cursor()
        c.execute('''
                  INSERT INTO Dates (date) values
                  (?);
                  ''',(dates,))
        con.commit()
    except sqlite3.Error as error:
        print('Ошибка при работе sql', error)
    finally:
        if con:
            con.close()
            print('Соединение с sql закрыто')

def journals_insert(diary,dates_id,users_id):
    try:
        con= get_connection()
        with con:
            c = con.cursor()
        c.execute('''
                  INSERT INTO Journals(diary,dates_id,users_id) values
                  (?,?,?);
                  ''',(diary,dates_id,users_id,))
        con.commit()
    except sqlite3.Error as error:
        print('Ошибка при работе sql', error)
    finally:
        if con:
            con.close()
            print('Соединение с sql закрыто')


if __name__ == '__main__':
    users()
    dates()
    journals()
    # users_insert('Andrew', '1234')
    # dates_insert('2024-03-01')
    # journals_insert('test3', 3, 1)

