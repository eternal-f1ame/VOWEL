"""
Predict Preparation
"""
import cv2
from global_vars import model


def predict(thresholded):
    """
    This function is used to predict the gesture.
    """

    thresholded = cv2.resize(thresholded,(128,128))
    dictionary = {
        '[[1. 0. 0. 0. 0.]]':"front",
        '[[0. 1. 0. 0. 0.]]':"back",
        '[[0. 0. 1. 0. 0.]]':"left",
        '[[0. 0. 0. 1. 0.]]':"right",
        '[[0. 0. 0. 0. 1.]]':"stop",
        }

    image = thresholded.reshape(1,128,128,3)/255

    res = model.predict(image)
    key = str(res.round())
    keys = dictionary.keys()

    if key not in keys:
        return "none"

    return dictionary[key]

# EOL
