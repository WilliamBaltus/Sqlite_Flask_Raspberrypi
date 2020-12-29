import Adafruit_DHT
import time
import sqlite3
from sqlite3 import Error
import datetime


def insert_continuously_dht11(conn):
    sensor=Adafruit_DHT.DHT11 #set sensor type
    gpio=17 #gpio pin that signal will be read from
    #while True: #continuously collect and log DHT data into db
    humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio) #read data, if None, retry as per Adafruit method (5 times)
    
    if humidity is not None and temperature is not None: # if there is a reading
        temp_f = round((1.8*temperature + 32),2) 
        #print(' Temp={0:0.1f}°F  Humidity={1:0.1f}%'.format(temp_f, humidity))
    else: #wait 2 seconds and try reading again
        time.sleep(2)
        humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
        temp_f = round((1.8*temperature + 32),2)
        #print('Temp={0:0.1f}°F  Humidity={1:0.1f}%'.format(temp_f, humidity))
              
    unfiltered_timestamp = datetime.datetime.now()
    filtered_timestamp = unfiltered_timestamp - datetime.timedelta(microseconds = unfiltered_timestamp.microsecond)
    timestampStr = filtered_timestamp.strftime("%d-%b-%Y (%H:%M:%S)")
    print('Timestamp: ' + timestampStr + '   Temp: ' + str(temp_f) + '°F' + '    Humid: ' + str(humidity) + '%')
    dht11_data = (filtered_timestamp, temp_f, humidity) #pair data

    sql= ''' INSERT INTO dht11(timestamp, temp, humid) VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, dht11_data)
    conn.commit()
    time.sleep(1)

def create_connection(db_file): #connect to sqlite3 database
	conn = None
	try:
		conn = sqlite3.connect(db_file) #use sqlite method to connect, provide a path to a database as parameter
		return conn
	except Error as e:
		print(e)
	
	return conn

def main():
    #database path
    database = r"/home/pi/EE551_Final/dht11/sensors.db" #path where you want db to be created, and the name of db is up to you, it will be created if none exist
    # create a database connection
    conn = create_connection(database)
    insert_continuously_dht11(conn)
    
if __name__ == '__main__':
    main()


