import sqlite3
from sqlite3 import Error
import datetime
import Adafruit_DHT
import time
from flask import Flask, render_template

app = Flask(__name__) #instance of flask
    
def read_dht(conn): 
    sensor=Adafruit_DHT.DHT11 #set sensor type
    gpio=17 #gpio pin that signal will be read from 
    humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio) #read data, if None, retry as per Adafruit method (5 times)
    if humidity is not None and temperature is not None: # if there is a reading
        temp_f = round((1.8*temperature + 32),2)
    else: #wait 2 seconds and try reading again
        time.sleep(2)
        humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
        temp_f = round((1.8*temperature + 32),2)
    
    unfiltered_timestamp = datetime.datetime.now()
    filtered_timestamp = unfiltered_timestamp - datetime.timedelta(microseconds = unfiltered_timestamp.microsecond)# this rounds the time to the nearest second
    return (filtered_timestamp, temp_f, humidity) #return data    
    
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
        print (str(row[0])+"   Temp = "+str(row[1])+"F 	Humid = "+str(row[2]) +"%")

def run_flask(dht_data):
    @app.route('/') #index page
    def index():
        return render_template('index.html', **dht_data) #as per flask documentation, there needs to be .html code in a folder called templates within same directory

    
def main():
    database = r"/home/pi/EE551_Final/dht11/sensors.db" #path where you want db to be created, and the name of db is up to you, it will be created if none exist
	# create a database connection
    conn = create_connection(database)
    sql_create_dht11_table = """ CREATE TABLE IF NOT EXISTS dht11 (timestamp DATETIME,temp NUMERIC,humid NUMERIC); """
    
    # create tables
    if conn is not None:
        # create dht11 table if one does not exist
        create_table(conn, sql_create_dht11_table)
        #log newly read data into database
        insert_dht11(conn, read_dht(conn)) #insert into connected db
        #print latest data, just to verify
        select_data(conn)
        
        #read dht11
        time, temp, humid = read_dht(conn)
        #bundle data for flask to read properly
        data = {'time': time,'temp': temp,'humid': humid }
        #run web server
        run_flask(data)
        app.run(host='0.0.0.0', port=5000, debug=False) 

    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()
