import cv2
import numpy as np

video = cv2.VideoCapture(0)

YELLOW_MIN = np.array([15, 70, 115],np.uint8)
YELLOW_MAX = np.array([35, 255, 255],np.uint8)
# YELLOW_MAX = np.array([35, 255, 125],np.uint8)  ## Depending on the lighting this works better 

width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH ))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT ))
# Defined for cv2.line
height_upper = int(2*height//5)
height_lower = int(3*height//5)

output = 0
output_last_frame = 0

cY = 0
cX = 0

def banana_position():

    global output_last_frame

    while True:
        ret, frame = video.read()
        frame = cv2.flip(frame,1)

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        frame_threshed = cv2.inRange(hsv_frame, YELLOW_MIN, YELLOW_MAX)

        # cv2.line function takes as x=0, y=0 the upper left corner
        cv2.line(frame, (0, height_upper), (width, height_upper), (255, 255, 255), 1)
        cv2.line(frame, (0, height_lower), (width, height_lower), (255, 255, 255), 1)

        contours, _ = cv2.findContours(frame_threshed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) != 0:
            max_contour = max(contours, key = cv2.contourArea)
            max_area =  cv2.contourArea(max_contour)
            if max_area > 100:
                    cv2.drawContours(frame, max_contour, -1, (0, 255, 0), 2)

                    M = cv2.moments(max_contour)
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    # print(cX, cY)
                    cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)

        # output is for controlling the 
        if cY < height_upper:
            output = 1
        elif cY > height_lower:
            output = -1
        else:
            output = 0

        if output != output_last_frame:
            print(output)
            output_last_frame = output

        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    # video.stop()  esto para que?
    cv2.destroyAllWindows()

    return None

banana_position()
