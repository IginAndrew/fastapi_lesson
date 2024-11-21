import sqlite3


def get_connection():
    try:
        con = sqlite3.connect("db/journal.db")
        con.row_factory = sqlite3.Row
        print("Успешное подключение!")
        return con
    except Exception:
        print("Ошибка подключения!")


def users():
    con = get_connection()
    with con:
        c = con.cursor()
    c.execute(
        """
    CREATE TABLE IF NOT EXISTS Users
    (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT NOT NULL,
    psw TEXT NOT NULL,
    UNIQUE ("login") ON CONFLICT IGNORE
    );
    """
    )
    con.commit()


def dates():
    con = get_connection()
    with con:
        c = con.cursor()
    c.execute(
        """
    CREATE TABLE IF NOT EXISTS Dates
(
id INTEGER PRIMARY KEY AUTOINCREMENT,
date TEXT NOT NULL
);
    """
    )
    con.commit()


def journals():
    con = get_connection()
    with con:
        c = con.cursor()
    c.execute(
        """
    CREATE TABLE IF NOT EXISTS Journals
(
id INTEGER PRIMARY KEY AUTOINCREMENT,
diary TEXT,
dates_id INTEGER,
users_id INTEGER,
FOREIGN KEY (dates_id) REFERENCES Dates(id),
FOREIGN KEY (users_id) REFERENCES Users(id)
);
    """
    )
    con.commit()


def users_insert(login, psw):
    try:
        con = get_connection()
        with con:
            c = con.cursor()
        c.execute(
            """
                  INSERT INTO Users (login,psw) values
                  (?,?);
                  """,
            (
                login,
                psw,
            ),
        )
        con.commit()
    except sqlite3.Error as error:
        print("Ошибка при работе sql", error)
    finally:
        if con:
            con.close()
            print("Соединение с sql закрыто")


def dates_insert(dates):
    try:
        con = get_connection()
        with con:
            c = con.cursor()
        c.execute(
            """
                  INSERT INTO Dates (date) values
                  (?);
                  """,
            (dates,),
        )
        con.commit()
    except sqlite3.Error as error:
        print("Ошибка при работе sql", error)
    finally:
        if con:
            con.close()
            print("Соединение с sql закрыто")


def journals_insert(diary, dates_id, users_id):
    try:
        con = get_connection()
        with con:
            c = con.cursor()
        c.execute(
            """
                  INSERT INTO Journals(diary,dates_id,users_id) values
                  (?,?,?);
                  """,
            (
                diary,
                dates_id,
                users_id,
            ),
        )
        con.commit()
    except sqlite3.Error as error:
        print("Ошибка при работе sql", error)
    finally:
        if con:
            con.close()
            print("Соединение с sql закрыто")


def users_select_all():
    try:
        con = get_connection()
        with con:
            c = con.cursor()
        res = c.execute(
            """
        SELECT * FROM Users
        """
        )
        res = res.fetchall()
        if not res:
            print("No users")
            return False
        return res
    except sqlite3.Error as error:
        print("Error with SQLite in users_select_all", error)
    finally:
        if con:
            con.close()
            print("Connection closed")


def users_select(login):
    try:
        con = get_connection()
        with con:
            c = con.cursor()
        res = c.execute(
            """
        SELECT * FROM Users
        WHERE login = ?;
        """,
            (login,),
        )
        res = res.fetchall()
        if not res:
            print("No users")
            return False
        return res
    except sqlite3.Error as error:
        print("Error with SQLite in users_select", error)
    finally:
        if con:
            con.close()
            print("Connection closed")


def users_select_login(id):
    try:
        con = get_connection()
        with con:
            c = con.cursor()
        res = c.execute(
            """
        SELECT * FROM Users
        WHERE id = ?;
        """,
            (id,),
        )
        res = res.fetchone()
        if not res:
            print("No users")
            return False
        return res
    except sqlite3.Error as error:
        print("Error with SQLite in users_select", error)
    finally:
        if con:
            con.close()
            print("Connection closed")


def users_update(login, New_login):
    try:
        con = get_connection()
        with con:
            c = con.cursor()
        c.execute(
            """
                  UPDATE Users SET login = ?
                  WHERE login = ?;
                  """,
            (
                New_login,
                login,
            ),
        )
        con.commit()
    except sqlite3.Error as error:
        print("Ошибка при работе sql", error)
    finally:
        if con:
            con.close()
            print("Соединение с sql закрыто")


def date_select_all():
    try:
        con = get_connection()
        with con:
            c = con.cursor()
        res = c.execute(
            """
        SELECT * FROM Dates
        """
        )
        res = res.fetchall()
        if not res:
            print("No dates")
            return False
        return res
    except sqlite3.Error as error:
        print("Error with SQLite in date_select_all", error)
    finally:
        if con:
            con.close()
            print("Connection closed")


def journal_select_all():
    try:
        con = get_connection()
        with con:
            c = con.cursor()
        res = c.execute(
            """
        SELECT * FROM Journals
        """
        )
        res = res.fetchall()
        if not res:
            print("No journals")
            return False
        return res
    except sqlite3.Error as error:
        print("Error with SQLite in journal_select_all", error)
    finally:
        if con:
            con.close()
            print("Connection closed")


def users_del(login):
    try:
        con = get_connection()
        with con:
            c = con.cursor()
        c.execute(
            """
                  DELETE FROM Users
                  WHERE login = ?;
                  """,
            (login,),
        )
        con.commit()
    except sqlite3.Error as error:
        print("Ошибка при работе sql", error)
    finally:
        if con:
            con.close()
            print("Соединение с sql закрыто")


def journal_del_user(login):
    try:
        con = get_connection()
        with con:
            c = con.cursor()
        c.execute(
            """
                  DELETE FROM Journals
                  WHERE users_id = (SELECT id FROM Users WHERE login = ?);
                  """,
            (login,),
        )
        con.commit()
    except sqlite3.Error as error:
        print("Ошибка при работе sql", error)
    finally:
        if con:
            con.close()
            print("Соединение с sql закрыто")


def dates_select_all():
    try:
        con = get_connection()
        with con:
            c = con.cursor()
        res = c.execute(
            """
        SELECT * FROM Dates
        """
        )
        res = res.fetchall()
        if not res:
            print("No users")
            return False
        return res
    except sqlite3.Error as error:
        print("Error with SQLite in users_select_all", error)
    finally:
        if con:
            con.close()
            print("Connection closed")


def journal_select_one(users_id, dates_id):
    try:
        con = get_connection()
        with con:
            c = con.cursor()
        res = c.execute(
            """
        SELECT * FROM Journals
        WHERE users_id = ? AND dates_id = ?;
        """,
            (
                users_id,
                dates_id,
            ),
        )
        res = res.fetchone()
        if not res:
            print("No journals")
            return False
        return res
    except sqlite3.Error as error:
        print("Error with SQLite in journal_select_one", error)
    finally:
        if con:
            con.close()
            print("Connection closed")


def journal_update(diary, dates_id, users_id):
    try:
        con = get_connection()
        with con:
            c = con.cursor()
        c.execute(
            """
                  UPDATE Journals SET diary = ?
                  WHERE dates_id = ? AND users_id = ?;
                  """,
            (diary, dates_id, users_id),
        )
        con.commit()
    except sqlite3.Error as error:
        print("Ошибка при работе sql", error)
    finally:
        if con:
            con.close()
            print("Соединение с sql закрыто")


def journal_del_user_data(users_id, dates_id):
    try:
        con = get_connection()
        with con:
            c = con.cursor()
        c.execute(
            """
                  DELETE FROM Journals
                  WHERE users_id = ? AND dates_id = ?;
                  """,
            (
                users_id,
                dates_id,
            ),
        )
        con.commit()
    except sqlite3.Error as error:
        print("Ошибка при работе sql", error)
    finally:
        if con:
            con.close()
            print("Соединение с sql закрыто")


if __name__ == "__main__":
    users()
    dates()
    journals()
    # users_insert('Andrew', '1234')
    # dates_insert('2024-03-01')
    # journals_insert('test3', 3, 1)
    # u = (users_select('Andrew'))
    # print(u[0]['psw'])
    # print([i for name in users_select_all() for i in name])
    # users_update("string", "Sveta", "1234")
    users_del("string")
