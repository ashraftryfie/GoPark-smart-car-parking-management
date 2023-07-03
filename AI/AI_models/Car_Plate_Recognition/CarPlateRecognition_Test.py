import cv2
import imutils
from imutils import paths

import numpy as np
import pytesseract
import argparse
import easyocr

from skimage.segmentation import clear_border
from matplotlib import pyplot as plt

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

def getCarPlateNumber(carImagePath):
    # load the input image from disk and resize it
    image = cv2.imread(carImagePath)
    image = imutils.resize(image, width=600)

    # crop the plate to an independent image
    # plate_image_cropped = image[y:y+h, x:x+w]

    # crop the plate number to an independent image
    # plate_number_cropped = image[y:y+h, x+int(w/2):x+w+3]
    
    image = image[5:int(image.shape[0] - 5) ,int(image.shape[1]/2 - 12):int(image.shape[1])]

    # filename = 'C:/Users/yamen/Desktop/test.jpg'
    # cv2.imwrite(filename, image)
                
    reader = easyocr.Reader(['ar'], gpu=True)
    result = reader.readtext(image)
    return result[0][-2]

# print(getCarPlateNumber('C:/Users/yamen/Desktop/savedImage.jpg'))