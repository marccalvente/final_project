import cv2
import pandas as pd
import numpy as np

from datetime import date
import visualize_path

video = cv2.VideoCapture(0)

YELLOW_MIN = np.array([15, 70, 115],np.uint8)
YELLOW_MAX = np.array([35, 255, 255],np.uint8)
# YELLOW_MAX = np.array([35, 255, 125],np.uint8)  ## Depending on the lighting this works better 

cY = 0
cX = 0

positions_list = []

def track_position():

    global cY
    global cX

    global positions_list

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
                positions_list.append([cX, cY])
                cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)

        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cv2.destroyAllWindows()

    positions_series = pd.Series(positions_list)
    positions_series.to_csv(f"./data/{date.today().strftime('%Y_%m_%d')}_position_tracking.csv")
    return None

track_position()
## This has to be moved to a main.py file
visualize_path.plot_path(f"./data/{date.today().strftime('%Y_%m_%d')}_position_tracking.csv")

