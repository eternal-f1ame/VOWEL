from utils import *
from global_vars import *

def predict(thresholded):

    thresholded = cv2.resize(thresholded,(128,128))

    dict = {'[[0. 1. 0. 0. 0.]]':"front",
            '[[1. 0. 0. 0. 0.]]':"back",
            '[[0. 0. 1. 0. 0.]]':"left",
            '[[0. 0. 0. 1. 0.]]':"right",
            '[[0. 0. 0. 0. 1.]]':"stop",
            }

    image = thresholded.reshape(1,128,128,1)/255

    res = model.predict(image)

    key = str(res.round())

    keys = dict.keys()

    if key not in keys:

        return "none"
        
    return dict[key]

