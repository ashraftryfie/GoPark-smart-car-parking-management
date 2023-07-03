from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

img_width, img_height = 224, 224

CATEGORIES = ['beige','black','blue', 'brown', 'gray' ,'green', 'orange','red', 'silver', 'white', 'yellow']

model = load_model('AI/AI_models/Car_Color_Prediction/trained_model/color_model.h5')



def getCarColor(carImagePath):
    preprocessingImage = image.load_img(carImagePath, target_size=(img_width, img_height,3))
    preprocessingImage = image.img_to_array(preprocessingImage)
    preprocessingImage = np.expand_dims(preprocessingImage, axis=0)
    preprocessingImage = preprocessingImage.reshape(1,img_width, img_height,3)    
    result = model.predict(preprocessingImage, batch_size=1)
    car_color_index = np.argmax(result,axis=1)
    return CATEGORIES[car_color_index[0]]

# print(getCarColor('C:/Users/yamen/Desktop/aa2.jpg'))