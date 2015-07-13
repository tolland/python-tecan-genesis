#!/usr/bin/python

import serial
from time import sleep

import tecan_funcs

ser = serial.Serial(port='/dev/ttyUSB1', baudrate=9600, timeout=10, writeTimeout=10, interCharTimeout=10 )

while True:
    data = ser.read(1)
    if len(data) > 0:
        print 'Got:', data

    sleep(0.1)
    print 'not blocked'

ser.close()
