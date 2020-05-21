#!/usr/bin/python3
import sys
import Adafruit_DHT
import pyowm
import RPi.GPIO as GPIO
from flask import Flask, render_template
GPIO.setwarnings(False)

app = Flask(__name__)

@app.route('/')
def index():
    humidity, temperature = Adafruit_DHT.read_retry(22,4)
    owm = pyowm.OWM('b92409985ad3a1360f71b0fbf24b902d')
    observation = owm.weather_at_place("Iasi,RO")
    w = observation.get_weather()
    temp_info = w.get_temperature('celsius')
    temp_outside = temp_info['temp']
    temperature = '{:0.1f}'.format(temperature)
    humidity = '{:0.1f}'.format(humidity)
    return render_template('index.html',temperature = temperature, humidity = humidity,temp_outside = temp_outside)

if __name__ == '__main__':
	app.run(debug=True,port=4000,host='0.0.0.0')