from utils import *
# !/usr/bin/env python

class Turtle_cleaner():

    def __init__(self):
        
        self.pub=rospy.Publisher('/rover_diff_drive_controller/cmd_vel',Twist,queue_size=1)

        rospy.init_node('Turtle_cleaner',anonymous=True)
        
        self.vel_msg=Twist()
        
        self.rate=rospy.Rate(10)

    def front_back(self,res):
        
        speed=1
        
        dist=0.01
        
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
        
        angle=3
        
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

    
