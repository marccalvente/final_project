import cv2
import numpy as np
# from pynput.keyboard import Key, Controller
from pynput.mouse import Controller


video = cv2.VideoCapture(0)

YELLOW_MIN = np.array([15, 70, 115],np.uint8)
YELLOW_MAX = np.array([35, 255, 255],np.uint8)


width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH ))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT ))
# Defined for cv2.line
height_upper = int(2*height//5)
height_lower = int(3*height//5)


global banana_pos 
banana_pos = 0
banana_pos_last_frame = 0

cY = 0
cX = 0

x_list = []
y_list = []

def draw_grid(img, grid_shape, color=(0, 255, 0), thickness=1):
    h, w, _ = img.shape
    rows, cols = grid_shape
    dy, dx = h / rows, w / cols

    # draw vertical lines
    for x in np.linspace(start=dx, stop=w-dx, num=cols-1):
        x = int(round(x))
        cv2.line(img, (x, 0), (x, h), color=color, thickness=thickness)

    # draw horizontal lines
    for y in np.linspace(start=dy, stop=h-dy, num=rows-1):
        y = int(round(y))
        cv2.line(img, (0, y), (w, y), color=color, thickness=thickness)

    return img

def get_lines_position(img, grid_shape):
    h, w, _ = img.shape
    rows, cols = grid_shape

    # get x positions
    for x in np.linspace(start=0, stop=w, num=cols+1):
        x = int(round(x))
        x_list.append(x)

    # get y positions
    for y in np.linspace(start=0, stop=h, num=rows+1):
        y = int(round(y))
        y_list.append(y)

    return x_list, y_list

_, frame_for_shape = video.read()
x_list, y_list = get_lines_position(frame_for_shape, (3,10))

print(f"x_list = {x_list}")
print(f"y_list = {y_list}")

def banana_position():

    # keyboard = Controller()
    mouse = Controller()

    global cY
    global cX
    global banana_pos
    global banana_pos_last_frame

    while True:
        ret, frame = video.read()
        frame = cv2.flip(frame,1)

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        frame_threshed = cv2.inRange(hsv_frame, YELLOW_MIN, YELLOW_MAX)

        frame = draw_grid(frame, (3,10))

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

        # mouse.position = (cX/width*1920, cY/height*1080)

        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cv2.destroyAllWindows()

    return None

banana_position()
