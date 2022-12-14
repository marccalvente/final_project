import cv2
import pandas as pd
import numpy as np

from pynput.mouse import Controller


video = cv2.VideoCapture(0)

YELLOW_MIN = np.array([15, 70, 115],np.uint8)
YELLOW_MAX = np.array([35, 255, 255],np.uint8)
# YELLOW_MAX = np.array([35, 255, 125],np.uint8)  ## Depending on the lighting this works better 

width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH ))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT ))

cY = 0
cX = 0

positions_list = []

def banana_position():

    mouse = Controller()

    global cY
    global cX

    while True:
        ret, frame = video.read()
        frame = cv2.flip(frame,1)

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        frame_threshed = cv2.inRange(hsv_frame, YELLOW_MIN, YELLOW_MAX)

        contours, _ = cv2.findContours(frame_threshed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) != 0:
            max_contour = max(contours, key = cv2.contourArea)
            max_area =  cv2.contourArea(max_contour)
            if max_area > 2000:
                cv2.drawContours(frame, max_contour, -1, (0, 255, 0), 2)

                M = cv2.moments(max_contour)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)

        mouse.position = (cX/width*1920, cY/height*1080)

        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cv2.destroyAllWindows()

    return None

banana_position()

