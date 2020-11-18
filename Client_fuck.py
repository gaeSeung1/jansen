PORT = 6000

from http.client import HTTPConnection
import json
import time
import numpy as np
import RPi.GPIO as GPIO
from Time import Time
from sys import argv
import mpu9250_test as test

print(argv)

def main():
    #key init
    speed = 0
    HALF=0
    MOTOR_SPEEDS = {
        "q": (HALF, 1), "w": (1, 1), "e": (1, HALF),
        "a": (-1, 1), "s": (0, 0), "d": (1, -1),
        "z": (-HALF, -1), "x": (-1, -1), "c": (-1, -HALF),
    }

    #motor init

    GPIO.setmode(GPIO.BCM)
    motor11=23
    motor12=24
    motor21=27
    motor22=17
    pwm1=25
    pwm2=22

    GPIO.setup(motor11,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(motor12,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(motor21,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(motor22,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(pwm1,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(pwm2,GPIO.OUT,initial=GPIO.LOW)

    p1=GPIO.PWM(pwm1,100)
    p2=GPIO.PWM(pwm2,100)

    p1.start(0)
    p2.start(0)
        


    #PID init
    targetDeg = 0
    Kp = 3.
    Kd = 0.
    Ki = 0
    dt = 0.
    dt_sleep = 0.01
    tolerance = 0.01

    start_time = time.time()
    error_prev = 0.
    time_prev = 0.


    #socket 
    while True:
        conn = HTTPConnection(f"{argv[1] if len(argv) > 1 else  'localhost'}:{PORT}")

        try:
            conn.request("GET", "/")
        except ConnectionRefusedError as error:
            print(error)
            sleep(1)
            continue

        print('Connected')
        
        
        

        print("1")        
#Control start

        res = conn.getresponse()
        while True:                        
            #Key input
            print(res)
            chunk = res.readline()
            print("2")
            if (chunk == b'\n'): continue
            if (not chunk): break
            print(chunk)
            chunk = chunk[:-1].decode()
            data = json.loads(chunk)
            print(Time(), data)
            action = data['action']



main()
