#!/usr/bin/python3
import sys
import Adafruit_DHT
import pyowm
from RPLCD.gpio import CharLCD
import RPi.GPIO as GPIO
import datetime
import time
import RPi.GPIO as GPIO
import time
import smtplib
import getpass
GPIO.setwarnings(False)

smtpUser = raw_input('Gmail: ')
smtpPass = getpass.getpass('\nPassword: ')
toAdd = raw_input('\nMail to send info to: ')
room_temp = float(raw_input('\nDesired room temperature: '))
#smtpUser = 'teodorparfeni@gmail.com'
#smtpPass = 'Pentagon1809'
#toAdd = 'teodorparfeni@gmail.com'
fromAdd = smtpUser
subject = 'Temperature and humidity alert'
header = 'To: ' + toAdd + '\n' + 'From: ' + fromAdd + '\n' + 'Subject: ' + subject
s = smtplib.SMTP('smtp.gmail.com',587)
s.ehlo()
s.starttls()
s.ehlo()
s.login(smtpUser, smtpPass)

lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 23], numbering_mode=GPIO.BOARD)

owm = pyowm.OWM('b92409985ad3a1360f71b0fbf24b902d')
observation = owm.weather_at_place("Iasi,RO")

ok_hum_low = 0
ok_hum_high = 0
ok_temp_low = 0
ok_temp_high = 0
i = 0

while True:
	w = observation.get_weather()
	temperature = w.get_temperature('celsius')
	temp_local = temperature['temp']
	while i != 1:
	    print ('\nOutside temperature: ' + str(temp_local))
	    i = 1
	if ok_hum_high == 0:
		timp_vechi_hum_high = datetime.datetime.today()
	if ok_hum_low == 0:
		timp_vechi_hum_low = datetime.datetime.today()
	if ok_temp_high == 0:
		timp_vechi_temp_high = time.time()
	if ok_temp_low == 0:
		timp_vechi_temp_low = time.time()


	humidity, temperature = Adafruit_DHT.read_retry(22, 4)

	print ('\nTemp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity))

	lcd.cursor_pos = (0, 0)
	lcd.write_string("Temp: %0.1f C" % temperature)
	lcd.cursor_pos = (1, 0)
	lcd.write_string("Humidity: %0.1f %%" % humidity)

	if temp_local > 30:
                if humidity < 45 and ok_hum_low == 0:
                        print ('Low humidity')
                        body = 'Alert for low humidity: '
                        s.sendmail(fromAdd,toAdd,header+'\n\n' + body + str(humidity) +'%')
                        ok_hum_low = 1
                if humidity > 65 and ok_hum_high == 0:
                        print ('High humidity')
                        body = 'Alert for high humidity: '
                        s.sendmail(fromAdd,toAdd,header+'\n\n' + body + str(humidity) +'%')
                        ok_hum_high = 1


	if temp_local > 20 and temp_local < 30:
                if humidity < 40 and ok_hum_low == 0:
                        print ('Low humidity')
                        body = 'Alert for low humidity: '
                        s.sendmail(fromAdd,toAdd,header+'\n\n' + body + str(humidity) +'%')
                        ok_hum_low = 1
                if humidity > 60 and ok_hum_high == 0:
                        print ('High humidity')
                        body = 'Alert for high humidity: '
                        s.sendmail(fromAdd,toAdd,header+'\n\n' + body + str(humidity) +'%')
                        ok_hum_high = 1


	if temp_local > 10 and temp_local < 20:
		if humidity < 35 and ok_hum_low == 0:
			print ('Low humidity')
			body = 'Alert for low humidity: '
			s.sendmail(fromAdd,toAdd,header+'\n\n' + body + str(humidity) +'%')
			ok_hum_low = 1
		if humidity > 55 and ok_hum_high == 0:
			print ('High humidity')
			body = 'Alert for high humidity: '
			s.sendmail(fromAdd,toAdd,header+'\n\n' + body + str(humidity) +'%')
			ok_hum_high = 1


	if temp_local > 0 and temp_local < 10:
		if humidity < 30 and ok_hum_low == 0:
                        print ('Low humidity')
                        body = 'Alert for low humidity: '
                        s.sendmail(fromAdd,toAdd,header+'\n\n' + body + str(humidity) +'%')
                        ok_hum_low = 1
		if humidity > 50 and ok_hum_high == 0:
        		print ('High humidity')
			body = 'Alert for high humidity: '
			s.sendmail(fromAdd,toAdd,header+'\n\n' + body + str(humidity) +'%')
			ok_hum_high = 1
 

	if temp_local > -10 and temp_local < 0:
                if humidity < 25 and ok_hum_low == 0:
                        print ('Low humidity')
                        body = 'Alert for low humidity: '
                        s.sendmail(fromAdd,toAdd,header+'\n\n' + body + str(humidity) +'%')
                        ok_hum_low = 1
                if humidity > 45 and ok_hum_high == 0:
                        print ('High humidity')
                        body = 'Alert for high humidity: '
                        s.sendmail(fromAdd,toAdd,header+'\n\n' + body + str(humidity) +'%')
                        ok_hum_high = 1


	if temp_local < -10:
                if humidity < 20 and ok_hum_low == 0:
                        print ('Low humidity')
                        body = 'Alert for low humidity: '
                        s.sendmail(fromAdd,toAdd,header+'\n\n' + body + str(humidity) +'%')
                        ok_hum_low = 1
                if humidity > 40 and ok_hum_high == 0:
                        print ('High humidity')
                        body = 'Alert for high humidity: '
                        s.sendmail(fromAdd,toAdd,header+'\n\n' + body + str(humidity) +'%')
                        ok_hum_high = 1

	if temperature - room_temp >= 1 and ok_temp_high == 0:
	    if temp_local < room_temp:
		body = 'Stop heating: '
		print body
		s.sendmail(fromAdd,toAdd,header+'\n\n' + body + str(temperature) + 'C')
		ok_temp_high = 1
	    if temp_local > room_temp:
		body = 'Start AC: '
		print body
		s.sendmail(fromAdd,toAdd,header+'\n\n' + body + str(temperature) + 'C')
		ok_temp_high = 1
	if room_temp - temperature >= 1 and ok_temp_low == 0:
	    if temp_local < room_temp:
		body = 'Start heating: '
		print body
		s.sendmail(fromAdd,toAdd,header+'\n\n' + body + str(temperature) + 'C')
		ok_temp_low = 1
	    if temp_local > room_temp:
		body = 'Stop AC: '
		print body
		s.sendmail(fromAdd,toAdd,header+'\n\n' + body + str(temperature) + 'C')
		ok_temp_low = 1

	if ok_hum_low == 1:
	    if datetime.datetime.today().day > timp_vechi_hum_low.day:
		ok_hum_low = 0

	if ok_hum_high == 1:
	    if datetime.datetime.today().day > timp_vechi_hum_high.day:
		ok_hum_high = 0

	if ok_temp_low == 1:
	    if timp_vechi_temp_low - time.time() >= 3600:
		ok_temp_low =0

	if ok_temp_high == 1:
	    if timp_vechi_temp_high - time.time() >= 3600:
		ok_temp_high = 0

	time.sleep(1)