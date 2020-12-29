import sqlite3
from sqlite3 import Error
import datetime
import Adafruit_DHT
import time
from flask import Flask, render_template

app = Flask(__name__) #instance of flask
    
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

def get_data(): #utility function, returns data from db
    database = r"/home/pi/EE551_Final/dht11/sensors.db" #path where you want db to be created, and the name of db is up to you, it will be created if none exist
    # create a database connection
    conn = create_connection(database)
    select_latest= ''' SELECT * FROM dht11 ORDER BY timestamp DESC LIMIT 1 '''
    cur = conn.cursor()
    for row in cur.execute(select_latest):
        time = str(row[0])
        temp = row[1]
        humid = row[2]

    return time, temp, humid
        
def select_data_test(conn): #prints data
    select_latest= ''' SELECT * FROM dht11 ORDER BY timestamp DESC LIMIT 1 '''
    cur = conn.cursor()
    for row in cur.execute(select_latest):
        print (str(row[0])+"   Temp = "+str(row[1])+"F 	Humid = "+str(row[2]) +"%")

def run_flask():
    @app.route('/') #index page
    def index():
        #get db data on each refresh
        time, temp, humid = get_data()
        #bundle data for flask to read properly
        dht_data = {'time': time,'temp': temp,'humid': humid }
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
        #print latest data, just to verify
        select_data_test(conn)
        #run web server
        run_flask()
        

    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()
    app.run(host='0.0.0.0', port=5000, debug=False) 