from utils import *
def count(thresholded, segmented):
  
    chull = cv2.convexHull(segmented)
    chullCopy = cv2.convexHull(segmented)
  
    extreme_top    = tuple(chull[chull[:, :, 1].argmin()][0])
    extreme_bottom = tuple(chull[chull[:, :, 1].argmax()][0])
    extreme_left   = tuple(chull[chull[:, :, 0].argmin()][0])
    extreme_right  = tuple(chull[chull[:, :, 0].argmax()][0])

    cX = int((extreme_left[0] + extreme_right[0]) / 2)
    cY = int((extreme_top[1] + extreme_bottom[1]) / 2)


    distance = pairwise.euclidean_distances([(cX, cY)], Y=[extreme_left, extreme_right, extreme_top, extreme_bottom])[0]
    maximum_distance = distance[distance.argmax()]

 
    radius = int(0.77 * maximum_distance)

  
    circumference = (2 * np.pi * radius)

    circular_roi = np.zeros(thresholded.shape[:2], dtype="uint8")
	
 
    cv2.circle(circular_roi, (cX, cY), radius, 255, 1)


    circular_roi = cv2.bitwise_and(thresholded, thresholded, mask=circular_roi)


    (cnts, _) = cv2.findContours(circular_roi.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    

    count = 0

 
    for c in cnts:
  
        (x, y, w, h) = cv2.boundingRect(c)


        if ((cY + (cY * 0.25)) > (y + h)) and ((circumference * 0.25) > c.shape[0]):
            count += 1

    return count,chullCopy



