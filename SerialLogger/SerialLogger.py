import serial
import sqlite3
from sqlite3 import Error

database = r"SensorLog.db"

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn


def create_table(conn):
    sql_create_table = """ CREATE TABLE IF NOT EXISTS env (
                                    id integer PRIMARY KEY,
                                    tempc text,
                                    tempf text,
                                    pressure text,
                                    humidity text,
                                    eco2 text,
                                    tvoc text
                                    ); """

    try:
        c = conn.cursor()
        c.execute(sql_create_table)
    except Error as e:
        print(e)


def insert_data(conn, vars):
    sql = ''' INSERT INTO env(tempc,tempf,pressure,humidity,eco2,tvoc)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, vars)
    conn.commit()
    return cur.lastrowid


def main():
    print("Sensor Logger");
    # create a database connection
    print(" - Creating connection to database");
    conn = create_connection(database)
    # create tables
    if conn is not None:
        print(" - Creating table if needed");
        create_table(conn)
        # Read serial port and log
        with serial.Serial('COM4', 115200) as ser:
            print(" - Opening serial port and logging");
            while True:
                line = ser.readline().strip()   # read a '\n' terminated line
                data = tuple(map(str, line.decode("utf-8").split(',')))
                series = insert_data(conn, data)
                print(" - Logging series: ", series, "\r", end="")
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
