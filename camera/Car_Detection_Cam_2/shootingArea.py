import cv2
import pickle
import numpy as np



try:
    with open('camera/Car_Detection_Cam_2/shooting area/Location_shooting_area', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []


def mouseClick(events, x, y, flags, params):

    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        posList.clear()


    with open('camera/Car_Detection_Cam_2/shooting area/Location_shooting_area', 'wb') as f:
        pickle.dump(posList, f)


while True:
    img = cv2.imread('camera/Car_Detection_Cam_2/test3.jpg')

    if len(posList)>=4:
        pts = np.array([posList[0],posList[1],posList[2],posList[3]], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], True, (0, 255, 255))


    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick)
    key = cv2.waitKey(1)
    if key == 27:
        cv2.destroyAllWindows()
        break




