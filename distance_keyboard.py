import cv2
import numpy as np
from pynput.keyboard import Key, Controller
# from pynput import mouse, keyboard


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

font = cv2.FONT_HERSHEY_COMPLEX
fontScale = 1
color_text = (0,0,0)
thickness_text = 1

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


def get_letter_positions(x_list, y_list):
    letter_positions = []
    for i in range(len(x_list)-1):
        for j in range(len(y_list)-1):
            letter_positions.append((int((x_list[i]+x_list[i+1])/2), int((y_list[j]+y_list[j+1])/2)))
    return letter_positions


def get_square_limits(x_list, y_list):
    """
        inputs: x_list --> List of x positions of the divisions
                y_list --> List of y positions of the divisions
                
        output: a list containing dictionaries with the limits for each square of the grid following the pattern:
                [{x_min, x_max, y_min, y_max, character}, ...]
    """
    keyboard_characters = ['q', 'a', 'z', 'w', 's', 'x', 'e', 'd', 'c', 'r', 'f', 'v', 't', 'g', 'b', 'y', 'h', 'n', 'u', 'j', 'm', 'i', 'k', 'space', 'o', 'l', 'backspace', 'p', 'ñ', 'enter']
    list_grid = []
    for i in range(len(x_list)-1):
        for j in range(len(y_list)-1):
            list_grid.append({"x_min" : x_list[i], "x_max" : x_list[i+1], "y_min" : y_list[j], "y_max" : y_list[j+1]})

    for k in range(len(keyboard_characters)):
        list_grid[k]["key_to_press"] = keyboard_characters[k]
        
    return list_grid


def banana_position():

    keyboard = Controller()
    # mouse_controller = mouse.Controller()

    keyboard_characters = ['q', 'a', 'z', 'w', 's', 'x', 'e', 'd', 'c', 'r', 'f', 'v', 't', 'g', 'b', 'y', 'h', 'n', 'u', 'j', 'm', 'i', 'k', 'space', 'o', 'l', 'backspace', 'p', 'ñ', 'enter']

    global cY
    global cX
    global banana_pos
    global banana_pos_last_frame

    _, frame_ini = video.read()
    x_list, y_list = get_lines_position(frame_ini, (3,10))
    letter_positions = get_letter_positions(x_list, y_list)
    squares = get_square_limits (x_list, y_list)
    print(x_list)
    print(y_list)

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

        frame = draw_grid(frame, (3,10))
        
        for i in range(len(keyboard_characters)):
            frame = cv2.putText(frame, keyboard_characters[i], letter_positions[i], font, fontScale, color_text, thickness_text, cv2.LINE_AA)

        for square in squares:
            if (cX > square["x_min"]) and (cX < square["x_max"]) and (cY > square["y_min"]) and (cY < square["y_max"]):
                if square["key_to_press"] == "space":
                    keyboard.press(Key.space)
                    keyboard.release(Key.space)

                elif square["key_to_press"] == "backspace":
                    keyboard.press(Key.backspace)
                    keyboard.release(Key.backspace)

                elif square["key_to_press"] == "enter":
                    keyboard.press(Key.enter)
                    keyboard.release(Key.enter)
                    
                else:
                    keyboard.press(f'{square["key_to_press"]}')
                    keyboard.release(f'{square["key_to_press"]}')

        # mouse_controller.position = (cX/width*1920, cY/height*1080)

        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cv2.destroyAllWindows()

    return None

banana_position()
