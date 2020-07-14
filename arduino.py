import struct
import serial
import RPi.GPIO as GPIO
import time
import csv
import os
from datetime import datetime, timedelta
lastMeasured = 0
lastWatered = 0
water_seconds = 43200
measure_seconds = 10800
water_seconds

def readSerial(triggertype):
        ser_bytes = ser.readline()
        decoded_bytes = ser_bytes[0:len(ser_bytes)-2].decode("utf-8")
        print(decoded_bytes)
        getSerial(decoded_bytes, triggertype)

def splitByWord(searchword, decoded_bytes):
        val = 0
        if searchword in decoded_bytes:
                for word in decoded_bytes.split():
                        if word.isdigit():
                                val = float(word)
        return val                                                                                                                                                                                                                                                                                                                                                                                                                                                                        def getSerial(decoded_bytes, triggertype):                                                                                                                                                                                                       num=0
    writeToFile("full_log.csv", decoded_bytes)
    num = splitByWord("moisture", decoded_bytes)
    writeToFile("percentage_log.csv", num)

    if triggertype == 2:
        bool = splitByWord("water", decoded_bytes)
        writeToFile("last_watered_log.csv", bool)

def writeToFile(filename, data):
        with open(filename,"a") as f:
                writer = csv.writer(f,delimiter=",")
                writer.writerow([time.time(), data])

try:
        ser=serial.Serial("/dev/ttyACM0",9600)  #change ACM number as found from ls /dev/tty*
        ser.baudrate=9600
        ser.flushInput()
except:
    print("arduino not found!")

def readFromFile(filename, triggertype, loopcount):
    global lastMeasured
    global lastWatered
    if os.path.isfile(filename):
        with open(filename, "r") as f:
            last_line = f.readlines()[-1]
            word = last_line.split(',')[0]
            if triggertype == 1:
                lastMeasured = float(word)
            elif triggertype == 2:
                lastWatered = float(word)

    else:
        checkWrite(triggertype, loopcount)

def checkWrite(triggertype, loopcount):
    if triggertype == 1:
        ser.write(b'1')
    elif triggertype == 2:
        ser.write(b'2')

    for x in range(0,loopcount):
        readSerial(triggertype)

def timer(measuredTime, statictime, triggertype, loopcount):
    deltaT = time.time() - measuredTime
    if deltaT >= statictime and measuredTime != 0:
        checkWrite(triggertype, loopcount)
        #check here if it needs to be watered and then water it here with ser.write(b'1')
while True:
        try:
            readFromFile('./full_log.csv', 1, 5)
            readFromFile('./last_watered_log.csv', 2, 6)

            timer(lastMeasured, measure_seconds, 1, 5)
            timer(lastWatered, water_seconds, 2, 6)                                                                                                                                                                                                                                                                                                                                                                                                                                               #except:                                                                                                                                                                                                                                        # print("Keyboard Interrupt")
        except:
            print("Keyboard Interrupt")
            break