import cv2
import numpy as np

video = cv2.VideoCapture(0)
# video = cv2.VideoCapture("./data/banana_horizontal.mp4")

YELLOW_MIN = np.array([15, 70, 70],np.uint8)
YELLOW_MAX = np.array([35, 255, 255],np.uint8)

while True:
    ret, frame = video.read()

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frame_threshed = cv2.inRange(hsv_frame, YELLOW_MIN, YELLOW_MAX)

    cv2.imshow("Frame", frame_threshed)

    key = cv2.waitKey(1) & 0XFF
    if key == ord('q'):
        break

# video.stop()
cv2.destroyAllWindows()




#hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

