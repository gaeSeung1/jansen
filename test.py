PORT = 5000

from http.client import HTTPConnection
import json
import time
import numpy as np
import RPi.GPIO as GPIO
from Time import Time
from sys import argv
import mpu9250_test as test


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
    
#MPU init

# Set up class
gyro = 250      # 250, 500, 1000, 2000 [deg/s]
acc = 2         # 2, 4, 7, 16 [g]
tau = 0.98
mpu = test.MPU(gyro, acc, tau)

# Set up sensor and calibrate gyro with N points
mpu.setUp()
mpu.calibrateGyro(500)


#PID init
targetDeg = 0
Kp = 5.
Kd = 0.
Ki = 0
dt = 0.
dt_sleep = 0.01
tolerance = 0.01

start_time = time.time()
error_prev = 0.
time_prev = 0.


#Control start

while True:
    #PID_init
    motorDeg = mpu.compFilter()
    error = targetDeg - motorDeg
    de = error-error_prev
    dt = time.time() - time_prev
    control = Kp*error + Kd*de/dt + Ki*error*dt
    error_prev = error
    time_prev = time.time()

    #motor control

    pw1 = 50
    pw2 = 50

    pw1_PID = max(min((abs(pw1) - control),100),0)  

    #direction
    if pw1>0:
        GPIO.output(motor11,GPIO.HIGH)
        GPIO.output(motor12,GPIO.LOW)
    elif pw1<0:
        GPIO.output(motor11,GPIO.LOW)
        GPIO.output(motor12,GPIO.HIGH)
    if pw2>0:
        GPIO.output(motor21,GPIO.HIGH)
        GPIO.output(motor22,GPIO.LOW)
    elif pw2<0:
        GPIO.output(motor21,GPIO.LOW)
        GPIO.output(motor22,GPIO.HIGH)  

    #PID control   
    if abs(error) >= tolerance:                 
        p1.ChangeDutyCycle(pw1_PID)
        p2.ChangeDutyCycle(abs(pw2))
        
    print("motorDeg :", motorDeg)
    print(pw1_PID, abs(pw2))
    time.sleep(dt_sleep)    
                            
    