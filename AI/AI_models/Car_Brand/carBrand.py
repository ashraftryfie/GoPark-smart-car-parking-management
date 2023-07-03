from tensorflow import keras
import matplotlib.pyplot as plt
import numpy as np
import cv2
from PIL import Image


model_path = "AI/AI_models/Car_Brand/trained_model/model_type_car.h5"

loaded_model = keras.models.load_model(model_path)

def getCarBrand(image_path):
    image = cv2.imread(image_path)
    image_fromarray = Image.fromarray(image, 'RGB')
    resize_image = image_fromarray.resize((128, 128))
    expand_input = np.expand_dims(resize_image, axis=0)
    input_data = np.array(expand_input)
    input_data = input_data/255
    pred = loaded_model.predict(input_data)
    result = pred.argmax()
    brand, model = 'Unknown', 'Unknown'

    if result == 0:
        brand = "Hyundai" 
        model = "Avante"

    elif result == 1:
        brand = "SABA"

    elif result == 2:
        brand = "Audi"

    elif result == 3:
        brand = "Benz"

    elif result == 4:
        brand = "KIA"
        model = "Rio"

    elif result == 5:
        brand = "KIA"
        model = "Forte"

    return brand, model

# print(getCarBrand('C:/Users/yamen/Desktop/aa2.jpg'))