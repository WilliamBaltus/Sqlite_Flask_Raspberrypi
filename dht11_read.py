import Adafruit_DHT
import time
 
# Set sensor -type : Options are DHT11,DHT22 or AM2302
sensor=Adafruit_DHT.DHT11
 
# Set GPIO sensor is connected to
gpio=17   
 
# Use read_retry method. This will retry up to 15 times to
# get a sensor reading (waiting 2 seconds between each retry).

 
# Reading the DHT11 is very sensitive to timings and occasionally
# the Pi might fail to get a valid reading. So check if readings are valid.
while True:
  humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
  if humidity is not None and temperature is not None:
    temp_f = 1.8*temperature + 32
    print('Temp={0:0.1f}°C  Humidity={1:0.1f}%'.format(temp_f, humidity))
  else:
    print('Failed to get reading. Try again!')
  time.sleep(2)
