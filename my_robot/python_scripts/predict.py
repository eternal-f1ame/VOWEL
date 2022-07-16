"""
Predict Preparation
"""
import json
import cv2
from tensorflow.keras.models import load_model

model = load_model('model/saved/resnet_model.h5')

with open('configurations.json', encoding="utf-8") as load_value:
    configurations = json.load(load_value)

with open(configurations["MODEL_DIR"] +
"/" + "model_specifications.json", encoding="utf-8") as specs:
    model_config = json.load(specs)

_height = model_config["HEIGHT"]
_width = model_config["WIDTH"]

def predict(image):
    """
    This function is used to predict the gesture.
    """

    image = cv2.resize(image,(_height,_width))

    # Defining the Key value pairs for the model
    dictionary = {
        '[[1. 0. 0. 0. 0.]]':"front",
        '[[0. 1. 0. 0. 0.]]':"back",
        '[[0. 0. 1. 0. 0.]]':"left",
        '[[0. 0. 0. 1. 0.]]':"right",
        '[[0. 0. 0. 0. 1.]]':"stop",
        }

    # Reshaping the image to the required shape and for display purposes
    image = image.reshape(1,_height,_width,3)/255.0
    res = model.predict(image)

    # Rounding off the result to get the key value pair
    key = str(res.round())
    keys = dictionary.keys()

    # Checking if the key is in the dictionary
    if key not in keys:
        return "none"

    return dictionary[key]

# EOL
