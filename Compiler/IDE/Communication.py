import time
import serial
import sys
sys.path.append("..")
ser = None


def send_serial(text):
    time.sleep(3)
    ser.write(text.encode())


def open_serial():
    global ser
    ser = serial.Serial("COM5", 9600)


def close_serial():
    ser.close()