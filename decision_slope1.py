PORT = 6000

import cv2
import numpy as np
import time
import math
import glob
import os
import image_process as img

from http.client import HTTPConnection
import json
import sys

def set_path3(image, forward_criteria):
    height, width, channel = image.shape # height = 높이, width = 넓이, channel = 채널 (미사용)
    # print(height, width, channel)
    height = height-1
    width = width-1
    center=int(width/2)
    left=0
    right=width
    #이미지 크기 = 320x240 기준
    
    center = int((left+right)/2)        
    
    try:
        # 왼쪽 경계 결정
        if image[height][:center].min(axis=0) == 255:
            left = 0
        else:
            left = image[height][:center].argmin(axis=0)
        
        #오른쪽 경계 설정
        if image[height][center:].max(axis=0) == 0:
            right = width
        else:    
            right = center+image[height][center:].argmax(axis=0)  
        
        #중앙값 모음
        center = int((left+right)/2)
        
        #print(int(first_nonzero(image[:,center],0,height)))
        forward = min(int(height), int(first_nonzero(image[:,center],0,height))-1)
        #print(height, first_nonzero(image[:,center],0,height))
        
        left_line = first_nonzero(image[height-forward:height,center:],1, width-center)
        right_line = first_nonzero(np.fliplr(image[height-forward:height,:center]),1, center)
        
        center_y = (np.ones(forward)*2*center-left_line+right_line)/2-center
        center_x = np.vstack((np.arange(forward), np.zeros(forward)))

        # 앞 짧은 거리 직진 결정
        forward_check_number = 45 
        m2, c2 = np.linalg.lstsq(center_x(1:forward_check_number).T, center_y(1:forward_check_number), rcond=-1)[0]
        if abs(m2) < 0.35:
            short_forward = 'yes'
        else:
            short_forward = 'no'
        
        m, c = np.linalg.lstsq(center_x.T, center_y, rcond=-1)[0]
        if forward < 20 or forward < 50 and abs(m) < 0.35:
            result = 'backward'
        elif abs(m) < forward_criteria:
            result = 'forward'
        elif m > 0:
            result = 'left'
        elif m <= 0:
            result = 'right'
        else:
            result = 'forward' # 혹시 다른 예외 상황이 있을 시 코드 추가 가능

    except:
        print('Try문에 Error 발생')
        result = 'error_backward'
        m = 0
        forward = 'Error'
        short_forward = 'Error'
    
    return result, round(m,4), forward, short_forward

# 현재 있는 구간 설정
def path_finding(path_number, display):
    if path_number = 0:
        status = 'Normal'

    elif path_number = 1:
        status = 'Zigzag'

    return status 

# 기울기 -> 모터 속도 반환
def slope2motor(result, slope):
    HALF = 0 # 회전시 회전의 구심점이 되는 모터 속도, 기본값은 0 (정지)
    SPEED_STANDARD = 3 # 한쪽 방향으로 극회전해야하는 측정 기울기 기준, 기본값 3

    if      m >  SPEED_STANDARD:
        MOTOR_SPEED = (HALF, 1)
    elif    m < -SPEED_STANDARD:
        MOTOR_SPEED = (1, HALF)
    else:
        if slope == 0:
            MOTOR_SPEED = (0.5, 0.5)
        elif result == 'left':
            MOTOR_SPEED = ( (3 - slope)/3, slope/3)
        else: # result = 'right'
            MOTOR_SPEED = ( (-1)*slope/3, (3 + slope )/3 )
        
    return MOTOR_SPEED

# 직진 명령
# def go_straight(result, slope, forward, short_forward)
#    if result == 'left':






#motor init (모터)
GPIO.setmode(GPIO.BCM)
motor11=23
motor12=24
motor21=27
motor22=17
pwm1=25
pwm2=22

#GPIO
GPIO.setup(motor11,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(motor12,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(motor21,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(motor22,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(pwm1,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(pwm2,GPIO.OUT,initial=GPIO.LOW)
    
path_number = 0 #구간 넘버, 밑 주석 그림 참조
default_speed = 100 # 모터 조정 속도


# 길 구간
# 시험 기준
# 1구간 : 0 - 3
# 2구간 : 3 - 5
#  __________________________________________________________________________________________
# /
#|    1                                                                                     0
#|    _______________________________________________________________________________________  
#|          \ /                      \ /                                                    \
#|           |                        |     5                                               |
#\_____      |        __________      |     ___________________________________________     |                                            |
#/           |       /                |                                                \    |
#|           |       | (3으로 변경)    |                                                |    |
#|     _____/        \_______________/ \____________________        ___________________/    |
#|                                                                                          |
#|     2                                               4                                    |
#\__________________________________________________________        ________________________/

# 중간에 구간에서 재시작할 수 있는 경우를 고려해
# sys.argv로 시작하는 path_number를 설정한다.
if sys.argv[0] != 0:
    path_number = sys.argv[0]

while True:
    imagetest = cv2.imread('1125193134.jpg')
    display = set_path3(imagetest, 6)

    if path_number == 0: #구간 0-1 사이에 있음
        result, slope, forward, short_forward = set_path3(image, 5)
        MOTOR_SPEED = slope2motor(result, slope)
        MOTOR_SPEED = default_speed*MOTOR_SPEED
        p1.ChangeDutyCycle(abs(MOTOR_SPEED[0]))
        p2.ChangeDutyCycle(abs(MOTOR_SPEED[1]))
        if short_forward == 'no' and result = 'left':
            path_number = 1 # 구간 '1'로 전환
    elif: path number == 1 # 구간 1-2 사이에 있음
        result, slope, forward, short_forward = set_path3(image, 5)




    