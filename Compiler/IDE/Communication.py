import time
import serial
import sys
import threading

sys.path.append("..")

ser = None
thread = None

messages = []


def divide_message(message):
    for i in range(0, len(message), 32):
        segment = message[i:i+32]
        messages.append(segment)


def send_serial():
    global thread

    while len(messages) != 0:
        time.sleep(2)
        ser.write(messages[0].encode())

        while True:
            if ser.in_waiting > 0:
                response = ser.readline().decode().strip()
                print("Message received: ", response)
                if response == "RTR":
                    break

        messages.pop(0)

    thread = None


def pre_send_serial(text):
    divide_message(text)

    global thread

    if thread is None:
        thread = threading.Thread(target=send_serial)

    thread.start()


def open_serial():
    global ser
    if ser is None:
        ser = serial.Serial("COM3", 9600)


def close_serial():
    ser.close()
