import time
import serial
import sys
sys.path.append("..")
ser = None


def send_serial(text):
    time.sleep(2)
    ser.write(text.encode('ascii'))


def open_serial():
    global ser
    ser = serial.Serial("COM3", 9600)


def close_serial():
    ser.close()