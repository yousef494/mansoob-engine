#!/usr/bin/python

#This script communicate with gpio to run the ulterasonic sensor
#It returns the distance from the sensor to the facing object


import time
import RPi.GPIO as gpio


def read():
	gpio.setmode(gpio.BCM)
	GPIO_TRIG = 23
	GPIO_ECHO = 24
	gpio.setup(GPIO_TRIG,gpio.OUT)
	gpio.setup(GPIO_ECHO,gpio.IN)

	gpio.output(GPIO_TRIG,False)
	time.sleep(0.5)
	gpio.output(GPIO_TRIG,True)
	time.sleep(0.00001)
	gpio.output(GPIO_TRIG,False)

	start_time = time.time()
	stop_time = time.time()
	while gpio.input(GPIO_ECHO)==0:
		start_time = time.time()
	
	while gpio.input(GPIO_ECHO)==1:
		stop_time = time.time()
	
	elapsed = stop_time - start_time
#	print "%f" % elapsed
	distance = elapsed * 17150
	distance = int(distance)

	time.sleep(0.5)
	gpio.cleanup()
	return str(distance)


if __name__ == "__main__":
	print("Ulterasonic Measurement")
	result = read()
	print(result)
