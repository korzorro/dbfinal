import sqlite3

database = 'suggestion_box.db'
sqlite_script = 'create_db.sqlite'


if __name__ == '__main__':
    with sqlite3.connect(database) as conn:
        with open(sqlite_script) as sqlite_file:
            for command in sqlite_file.read().split(';'):
                conn.execute(command)
            conn.commit()
        
