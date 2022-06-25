from data.assets.utils import *

def segment(image,bg,threshold = 25):
    
    diff = cv2.absdiff(bg.astype("uint8"),image)

    thresholded = cv2.threshold(diff,threshold,255,cv2.THRESH_BINARY)[1]

    clone = thresholded.copy()

    (cnts,_) = cv2.findContours(clone,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    if len(cnts) == 0:

        return

    else:

        segmented = max(cnts,key=cv2.contourArea)

        return (thresholded,segmented)    


