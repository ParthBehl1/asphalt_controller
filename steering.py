import numpy as np
import cv2
import imutils
from imutils.video import VideoStream
import time
import pyautogui

cam = VideoStream(src=0).start()
currentKey = []

while True:
    key = False

    img = cam.read()
    img = imutils.resize(img, width=640, height=480)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    value = (11, 11)
    blurred = cv2.GaussianBlur(hsv, value, 0)
    colourLower = np.array([35, 71, 101])
    colourUpper = np.array([180, 255, 255])

    height = img.shape[0]
    width = img.shape[1]

    mask = cv2.inRange(blurred, colourLower, colourUpper)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))

    upContour = mask[0:height//2, 0:width]
    downContour = mask[3*height//4:height, 2*width//5:3*width//5]

    cnts_up = cv2.findContours(upContour, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts_up = imutils.grab_contours(cnts_up)

    cnts_down = cv2.findContours(downContour, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts_down = imutils.grab_contours(cnts_down)

    if len(cnts_up) > 0:
        c = max(cnts_up, key=cv2.contourArea)
        M = cv2.moments(c)
        cX = int(M["m10"] / (M["m00"]))

        if cX < (width//2 - 28):
            pyautogui.press('a')
            print("Pressed A")
            key = True
            currentKey.append('A')
        elif cX > (width//2 + 28):
            pyautogui.press('d')
            print("Pressed D")
            key = True
            currentKey.append('D')
            
    if len(cnts_down) > 0:
        pyautogui.press('space')
        print("Pressed Space for Nitro")
        key = True
        currentKey.append('Space')         

    img = cv2.rectangle(img, (0, 0), (width//2 - 28, height//2), (0, 255, 0), 1)
    cv2.putText(img, 'LEFT', (110, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0))

    img = cv2.rectangle(img, (width//2 + 28, 0), (width - 2, height//2), (0, 255, 0), 1)
    cv2.putText(img, 'RIGHT', (550, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0))

    img = cv2.rectangle(img, (2*(width//5), 3*(height//4)), (3*width//5, height), (0, 255, 0), 1)
    cv2.putText(img, 'NITRO', (2*(width//5) + 15, height - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0))


    cv2.imshow("Steering", img)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

    if not key and len(currentKey)!= 0:
        for current in currentKey:
            if current == 'A':
                pyautogui.press('a')
            elif current == 'D':
                pyautogui.press('d')
            elif current == 'Space':
                pyautogui.press('space')
            print("Released", current)
        currentKey = []

cv2.destroyAllWindows()
