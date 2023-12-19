import sqlite3
from sqlite3 import Error

class dataBase():
    def create_connection(db_file):
        try:
            conn = sqlite3.connect(db_file)
            cur = conn.cursor()
            res = cur.execute("CREATE TABLE movie(title, year, score)")
            res.fetchone()
        except Error as e:
            print(e)
        finally:
            if (conn):
                conn.close()


    if __name__ == '__main__':
        create_connection('..\EnergyBD.db')