import sqlite3

database = 'suggestion_box.db'
sqlite_script = 'create_db.sqlite'


if __name__ == '__main__':
    with sqlite3.connect(database) as conn:
        with open(sqlite_script) as sqlite_file:
            conn.executescript(sqlite_file.read())
            conn.commit()
