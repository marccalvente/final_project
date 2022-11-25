import cv2
import numpy as np

video = cv2.VideoCapture(0)
# video = cv2.VideoCapture("./data/banana_horizontal.mp4")

YELLOW_MIN = np.array([15, 75, 75],np.uint8)
YELLOW_MAX = np.array([35, 255, 255],np.uint8)

while True:
    ret, frame = video.read()

    frame_threshed = cv2.inRange(frame, YELLOW_MIN, YELLOW_MAX)

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1) & 0XFF
    if key == ord('q'):
        break

# video.stop()
cv2.destroyAllWindows()


