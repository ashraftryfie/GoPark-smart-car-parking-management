import cv2
import pickle
import cvzone
import numpy as np
import requests

import time



timer = time.time() - 16666666666

cap = cv2.VideoCapture('camera/Car_Detection_Cam_1/test.mp4')

with open('camera/Car_Detection_Cam_1/shooting area/Location_shooting_area', 'rb') as f:
    posList = pickle.load(f)

val1 = 45
val2 = 16
val3 = 15

isnew = True  ## To make sure a new car arrives


def checkSpace():
    global isnew, timer
    pts = np.array([posList[0], posList[1], posList[2], posList[3]], np.int32)
    ## (1) Crop the bounding rect
    rect = cv2.boundingRect(pts)
    x, y, w, h = rect
    croped = imgThres[y:y + h, x:x + w].copy()

    ## (2) make mask
    pts = pts - pts.min(axis=0)
    mask = np.zeros(croped.shape[:2], np.uint8)
    cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)

    ## (3) do bit-op
    imgCrop = cv2.bitwise_and(croped, croped, mask=mask)

    count = cv2.countNonZero(imgCrop)

    if count < 9000:
        color = (0, 0, 200)
        isnew = True
        spaces = "no"
    else:
        spaces = "yes"
        if isnew:
            if time.time() - timer > 20:
                # filename = 'camera/Car_Detection_Cam_1/carimage/savedImage.jpg'
                filename = 'AI/AI_models/YOLOv5/cars_entering/car.jpg'
                cv2.imwrite(filename, img)
                payload = {'imagePath': filename}
                result = requests.post('http://127.0.0.1:8000/AI/carIsEntering', data=payload)
                isnew = False

                timer = time.time()

        color = (0, 200, 0)

    pts = np.array([posList[0], posList[1], posList[2], posList[3]], np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv2.polylines(img, [pts], True, (0, 255, 255))

    cv2.putText(img, str(count), (posList[0][0], posList[0][1]), cv2.FONT_HERSHEY_PLAIN, 1,
                color, 2)

    cvzone.putTextRect(img, f'Having a car in the area: {spaces}', (50, 60), thickness=3, offset=20,
                       colorR=color)


def test():
    pass

while True:

    # Get image frame
    success, img = cap.read()
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        # cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        break

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)

    imgThres = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY_INV, val1, val2)
    imgThres = cv2.medianBlur(imgThres, val3)

    kernel = np.ones((3, 3), np.uint8)
    imgThres = cv2.dilate(imgThres, kernel, iterations=1)

    checkSpace()

    # Display Output
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == 27:
        cv2.destroyAllWindows()
        break

    # if key == ord('r'):