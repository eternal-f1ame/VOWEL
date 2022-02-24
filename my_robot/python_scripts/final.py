#!/usr/bin/env python
# license removed for brevity
##Move in x direction straight line
import rospy
from geometry_msgs.msg import Twist
from tensorflow.keras.models import load_model
import cv2
import imutils
import numpy as np
from sklearn.metrics import pairwise
from sklearn.cluster import k_means
from tensorflow.keras.models import load_model
from tensorflow import convert_to_tensor

model=load_model('control/python_scripts/gest_recog')
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
                    #cv2.imwrite("stop motion"+ "\\"+"captured"+"\\"+'Frame'+str(fr)+'.jpg', clone)
                    #cv2.imwrite("stop motion"+ "\\"+"segmented"+"\\"+'Frame'+str(fr)+'.jpg', thresholded)
                    #fr += 1
                    fingerC = 0
                    #chullsum = chullK[0].astype("int")
                else:
                    fingerC += fingers
                    
                    #chullsum = np.vstack([np.array(chullsum),np.array(chulln)])
                #print(thresholded.shape)
                res = predict(thresholded) 
                cv2.putText(clone, str(int(fingers)), (70, 85), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                cv2.imshow("Thesholded", thresholded)
                #if (fingers!=prevfin):
                cv2.putText(clone,res, (70, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                num += 1
                if ( num%100==0):
                    camera.release()
                    # cv2.destroyAllWindows()
                    if res=='stop' or res=='none' :
                        cv2.destroyAllWindows()
                    return fingers,res
        prevfin = fingers
        cv2.rectangle(clone, (left, top), (right, bottom), (0,255,0), 2)     
        num_frames += 1
        #for i in range(len(chull)):
            #cv2.circle(clone, chull[i][0]+[right,0], radius=5, color=(0,0,255), thickness=5)
        cv2.imshow("Video Feed", clone)
        keypress = cv2.waitKey(1) & 0xFF
        if fr == 1000:
            break


class Turtle_cleaner():

    def __init__(self):
        self.pub=rospy.Publisher('/rover_diff_drive_controller/cmd_vel',Twist,queue_size=1)
        rospy.init_node('Turtle_cleaner',anonymous=True)
        self.vel_msg=Twist()
        self.rate=rospy.Rate(10)

    def front_back(self,res,fingers):
        speed=2
        dist=fingers
        if res=='front':
            self.vel_msg.linear.x=abs(speed)
        if res=='back':
            self.vel_msg.linear.x=-abs(speed)
        else:
            pass
        self.vel_msg.linear.y=0
        self.vel_msg.linear.z=0
        self.vel_msg.angular.x=0
        self.vel_msg.angular.y=0
        self.vel_msg.angular.z=0
        while not rospy.is_shutdown():
            t0=rospy.Time.now().to_sec()
            current_dist=0
            while (current_dist< dist):
                self.pub.publish(self.vel_msg)
                t1=rospy.Time.now().to_sec()
                current_dist=speed*(t1-t0)
                self.rate.sleep()
        #stop from publishing
            self.vel_msg.linear.x=0
            self.pub.publish(self.vel_msg)
            break
    def left_right(self,res):
        dir=res
        angular_speed=45
        angle=90
        angular_speed=angular_speed*3.14/180
        angle=angle*3.14/180
        rate=rospy.Rate(10)
        self.vel_msg.linear.y=0
        self.vel_msg.linear.z=0
        self.vel_msg.angular.x=0
        self.vel_msg.angular.y=0
        self.vel_msg.linear.x=0
        if dir=='left':
            self.vel_msg.angular.z=abs(angular_speed)
        else:
            self.vel_msg.angular.z=-abs(angular_speed)
        while not rospy.is_shutdown():
            t0=rospy.Time.now().secs
            current_angle=0
            while(current_angle<=angle):
                self.pub.publish(self.vel_msg)
                t1=rospy.Time.now().secs
                current_angle=0.4*angular_speed*(t1-t0)
                rate.sleep()
            else:
                self.vel_msg.angular.z=0
                self.pub.publish(self.vel_msg)
                break
    def cont_movement(self):
        
        while True :
            cv2.waitKey(2000)
            fingers,res=video()
            if (res=='front') or (res=='back'):
                self.front_back(res,fingers)
            if (res=='left') or (res=='right'):
                self.left_right(res)
            if (res=='stop'):
                quit()

if __name__ == '__main__':
    try:
        x=Turtle_cleaner()
        
    except rospy.ROSInterruptException:
        pass


