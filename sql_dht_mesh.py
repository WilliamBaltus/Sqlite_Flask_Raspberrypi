import sqlite3
from sqlite3 import Error
import datetime
import Adafruit_DHT
import time

def read_dht(conn): 
    sensor=Adafruit_DHT.DHT11 #set sensor type
    gpio=17 #gpio pin that signal will be read from 
    humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio) #read data, if None, retry as per Adafruit method (5 times)
    if humidity is not None and temperature is not None: # if there is a reading
        temp_f = 1.8*temperature + 32
    else: #wait 2 seconds and try reading again
        time.sleep(2)
        humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
        temp_f = 1.8*temperature + 32
    
    dht11_data = (datetime.datetime.now(), temp_f, humidity) #pair data
    insert_dht11(conn, dht11_data) #insert into connected db
    
    
def create_connection(db_file): #connect to sqlite3 database
	conn = None
	try:
		conn = sqlite3.connect(db_file) #use sqlite method to connect, provide a path to a database as parameter
		return conn
	except Error as e:
		print(e)
	
	return conn

def create_table(conn, create_table_sql): #create table within connected db
    try:
        c = conn.cursor() #cursor object of connected db, contains execute method
        c.execute(create_table_sql) #sql commands you would input in sqlite3. see parameter for more detail 
    except Error as e:
        print(e)

def insert_dht11(conn, data):
    sql= ''' INSERT INTO dht11(timestamp, temp, humid)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()
    #return cur.lastrowid #cursors function that returns ID of row 

def select_data(conn):
    select_latest= ''' SELECT * FROM dht11 ORDER BY timestamp DESC LIMIT 1 '''
    cur = conn.cursor()
    for row in cur.execute(select_latest):
        print (str(row[0])+"   Temp = "+str(row[1])+"	Humid = "+str(row[2]))
    
    
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
        #data = (datetime.datetime.now(), 20.7,35) 
        read_dht(conn) #read dht11 and log into database
        select_data(conn)

    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
