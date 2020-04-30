#!/usr/bin/python

#This script communicate with gpio to run the ulterasonic sensor
#It returns the distance from the sensor to the facing object


def read():
	return str(50)


if __name__ == "__main__":
	print("Fake Ulterasonic Measurement")
	result = read()
	print(result)
