import sqlite3
from sqlite3 import Error
import datetime

def create_connection(db_file):
	conn = None
	try:
		conn = sqlite3.connect(db_file)
		return conn
	except Error as e:
		print(e)
	
	return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor() #cursor object of connected db, contains execute method
        c.execute(create_table_sql) #sql commands you would input in sqlite3
    except Error as e:
        print(e)

def insert_dht11(conn, data):
    sql= ''' INSERT INTO dht11(timestamp, temp, humid)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()
    #return cur.lastrowid #cursors function that returns ID of row 

def main():
    database = r"/home/pi/Databases/db/sensors.db"
	# create a database connection
    conn = create_connection(database)
    
    sql_create_dht11_table = """ CREATE TABLE IF NOT EXISTS dht11 (
                                        timestamp DATETIME,
                                        temp NUMERIC,
                                        humid NUMERIC); """

    # create tables
    if conn is not None:
        # create dht11 table
        create_table(conn, sql_create_dht11_table)
	#insert data into row
	data = (datetime.datetime.now(), 20.5,30)
	insert_dht11(conn,data)

    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
