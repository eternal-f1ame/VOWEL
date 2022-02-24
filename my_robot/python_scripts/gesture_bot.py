#!/usr/bin/env python
# license removed for brevity
##Move in x direction straight line
import rospy
from geometry_msgs.msg import Twist
import cv2
import imutils
import numpy as np
from sklearn.metrics import pairwise
from sklearn.cluster import k_means

bg = None;

def RunAvg(image,aWeight):
    global bg
    if bg is None:
        bg = image.copy().astype("float")
        return

    cv2.accumulateWeighted(image,bg,aWeight)



def segment(image,threshold = 25):
    global bg
    
    diff = cv2.absdiff(bg.astype("uint8"),image)
    thresholded = cv2.threshold(diff,threshold,255,cv2.THRESH_BINARY)[1]
    clone = thresholded.copy()
    (cnts,_) = cv2.findContours(clone,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts) == 0:
        return
    else:
        segmented = max(cnts,key=cv2.contourArea)
        return (thresholded,segmented)    

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

def video():

    aWeight = 0.1

    camera = cv2.VideoCapture(0)


    top, right, bottom, left = 10, 350, 225, 590
    prevfin = 0
    fingers = 0
    num_frames = 0
    fr = 0
    num = 1
    finger_disp = 0
    fingerC = 0
    while(True):

        (grabbed, frame) = camera.read()


        frame = imutils.resize(frame, width=700)


        frame = cv2.flip(frame, 1)


        clone = frame.copy()

     
        (height, width) = frame.shape[:2]

      
        roi = frame[top:bottom, right:left]

       
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

      
        if num_frames < 30:
            RunAvg(gray, aWeight)
        else:
           
            hand = segment(gray)

            
            if hand is not None:
                
                (thresholded, segmented) = hand

            
                cv2.drawContours(clone, [segmented + (right, top)], -1, (0, 0, 255))
                
                fingers,chull = count(thresholded,segmented)
                #chulln = [x[0].tolist() for x in chull]
                
                

                if num % 10 == 0:
                    finger_disp = fingerC
                    #cv2.imwrite("right motion"+ "\\"+"captured"+"\\"+'Frame'+str(fr)+'.jpg', clone)
                    #cv2.imwrite("right motion"+ "\\"+"segmented"+"\\"+'Frame'+str(fr)+'.jpg', thresholded)
                    fingerC = 0
                    #chullsum = chullK[0].astype("int")
                    


                else:
                    fingerC += fingers
                    num += 1
                    #chullsum = np.vstack([np.array(chullsum),np.array(chulln)])
                

                cv2.putText(clone, str(int(fingers)), (70, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                cv2.imshow("Thesholded", thresholded)
                if ( num_frames%300==0):
                    camera.release()
                    cv2.destroyAllWindows()
                    return fingers
                

        prevfin = fingers
        cv2.rectangle(clone, (left, top), (right, bottom), (0,255,0), 2)
        
            
        num_frames += 1
        #for i in range(len(chull)):
            #cv2.circle(clone, chull[i][0]+[right,0], radius=5, color=(0,0,255), thickness=5)
        cv2.imshow("Video Feed", clone)
        
        
        
        keypress = cv2.waitKey(1) & 0xFF

        
        if fr == 800:
            break

    




def move_x():
  
    #create a new publisher. we specify the topic name, then type of message then the queue size
    fingers=video()
    print(fingers)
    pub = rospy.Publisher('/rover_diff_drive_controller/cmd_vel', Twist, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    vel_msg=Twist()
    input_speed=float(input('speed '))
    input_direction=input('dir ')
    input_distance=fingers

    if (input_direction=='x'):
        vel_msg.linear.x=(input_speed)
    else:
        vel_msg.linear.y=input_speed
    vel_msg.linear.z=0
    vel_msg.angular.y=0
    vel_msg.angular.z=0
    vel_msg.angular.x=0
    while not rospy.is_shutdown():
        t0=rospy.Time.now().to_sec()
        intial_d=0
        while(intial_d<input_distance):
            pub.publish(vel_msg)
            t1=rospy.Time.now().to_sec()
            intial_d=input_speed*(t1-t0)
        if(input_direction=='x'):
            vel_msg.linear.x=0
        else:
            vel_msg.linear.y=0
        pub.publish(vel_msg)
        break
    print('end')
if __name__ == '__main__':
    try:
        for i in range(3):
            move_x()
    except rospy.ROSInterruptException:
        pass