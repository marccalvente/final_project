import cv2
import numpy as np

video = cv2.VideoCapture(0)

YELLOW_MIN = np.array([15, 70, 40],np.uint8)
YELLOW_MAX = np.array([35, 255, 125],np.uint8)

# height =  480, width = 640

while True:
    ret, frame = video.read()

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frame_threshed = cv2.inRange(hsv_frame, YELLOW_MIN, YELLOW_MAX)

    contours, _ = cv2.findContours(frame_threshed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) != 0:
        max_contour = max(contours, key = cv2.contourArea)
        max_area =  cv2.contourArea(max_contour)
        if max_area > 100:
                cv2.drawContours(frame, max_contour, -1, (0, 255, 0), 2)

                M = cv2.moments(max_contour)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                print(cX, cY)
                cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)

    # for contour in contours:
    #     area =  cv2.contourArea(contour)
    #     if area > 100:
    #         cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)

    #         M = cv2.moments(contour)
    #         cX = int(M["m10"] / M["m00"])
    #         cY = int(M["m01"] / M["m00"])
    #         print(cX, cY)
    #         cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
 
    # cv2.imshow("Frame", frame_threshed)
    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# video.stop()  esto para que?
cv2.destroyAllWindows()

