import cv2
import numpy as np
import sys
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

# You should replace these 3 lines with the output in calibration step
DIM=(320, 240)
K=np.array([[93.16858864610276, 0.0, 150.8535602775792], [0.0, 91.92373264897513, 146.22342371914382], [0.0, 0.0, 1.0]])
D=np.array([[0.14136243954038377], [0.29925561973923737], [-0.321789761587799], [0.11936916962615352]])
  
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
# allow the camera to warmup
time.sleep(0.1)
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(frame, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    img = frame.array
	# show the frame
 
    cv2.imshow("Frame", img)
    key = cv2.waitKey(1) & 0xFF
	# clear the stream in preparation for the next frame
    rawCapture.truncate(0)
	# if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break