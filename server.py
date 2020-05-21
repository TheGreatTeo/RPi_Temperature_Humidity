#!/usr/bin/python3
import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
from flask import Flask, render_template
GPIO.setwarnings(False)

app = Flask(__name__)

@app.route('/')
def index():
    humidity, temperature = Adafruit_DHT.read_retry(22,4)
    temperature = '{:0.1f}'.format(temperature)
    humidity = '{:0.1f}'.format(humidity)
    return render_template('index.html',temperature = temperature, humidity = humidity)

if __name__ == '__main__':
	app.run(debug=True,port=4000,host='0.0.0.0')
