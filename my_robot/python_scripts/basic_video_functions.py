"""
All the fundamental webcam codes
"""
import sys
import cv2
import numpy as np
from sklearn.metrics import pairwise
sys.path.append("../")


def segment_image(image,_background,threshold = 25):
    """
    This function is used to segment the hand.
    """
    diff = cv2.absdiff(_background.astype("uint8"),image)
    thresholded = cv2.threshold(diff,threshold,255,cv2.THRESH_BINARY)[1]
    clone = thresholded.copy()
    (cnts,_) = cv2.findContours(clone,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    if len(cnts) == 0:
        return

    segmented = max(cnts,key=cv2.contourArea)
    return (thresholded,segmented)

def run_average(image,_aweight,_background):
    """
    This function is used to run the average background.
    """

    if _background is None:
        _background = image.copy().astype("float")
        return _background

    return cv2.accumulateWeighted(image,_background,_aweight)

def count_fingers(thresholded, segmented):
    """
    Returns segmented hand.
    """
    c_hull = cv2.convexHull(segmented)
    c_hull_copy = cv2.convexHull(segmented)

    extreme_top    = tuple(c_hull[c_hull[:, :, 1].argmin()][0])
    extreme_bottom = tuple(c_hull[c_hull[:, :, 1].argmax()][0])
    extreme_left   = tuple(c_hull[c_hull[:, :, 0].argmin()][0])
    extreme_right  = tuple(c_hull[c_hull[:, :, 0].argmax()][0])

    _cx = int((extreme_left[0] + extreme_right[0]) / 2)
    _cy = int((extreme_top[1] + extreme_bottom[1]) / 2)


    distance = pairwise.euclidean_distances(
        [(_cx, _cy)],
        Y=[extreme_left, extreme_right,
        extreme_top,
        extreme_bottom])[0]
    maximum_distance = distance[distance.argmax()]


    radius = int(0.77 * maximum_distance)
    circumference = (2 * np.pi * radius)
    circular_roi = np.zeros(thresholded.shape[:2], dtype="uint8")


    cv2.circle(circular_roi, (_cx, _cy), radius, 255, 1)
    circular_roi = cv2.bitwise_and(thresholded, thresholded, mask=circular_roi)
    (cnts, _) = cv2.findContours(circular_roi.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    count = 0
    for _c in cnts:

        (_, y, _, h) = cv2.boundingRect(_c)
        if ((_cy + (_cy * 0.25)) > (y + h)) and ((circumference * 0.25) > _c.shape[0]):
            count += 1

    return count,c_hull_copy

# EOL
