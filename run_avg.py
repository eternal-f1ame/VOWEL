from utils import *
def RunAvg(image,aWeight,bg):
    if bg is None:
        bg = image.copy().astype("float")
        return bg

    cv2.accumulateWeighted(image,bg,aWeight)