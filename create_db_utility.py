import sqlite3
from sqlite3 import Error

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

    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
