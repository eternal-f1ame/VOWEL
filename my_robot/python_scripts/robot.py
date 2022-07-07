"""
Robot Intializations
"""
import sys
import rospy
from geometry_msgs.msg import Twist

sys.path.append("../")
#!/usr/bin/env python
# -*- coding: utf-8 -*-
class TurtleCleaner():
    """
    This function is used to move the turtlebot forward, backward, left and right.
    """
    def __init__(self, robot_config):

        self.pub=rospy.Publisher('/rover_diff_drive_controller/cmd_vel',Twist,queue_size=1)
        rospy.init_node('TurtleCleaner',anonymous=True)
        self.vel_msg=Twist()
        self.rate=rospy.Rate(10)
        self.config=robot_config

    def front_back(self,res):
        """
        This function is used to move the turtlebot forward and backward.
        """

        if res=='front':
            self.vel_msg.linear.x=abs(self.config["linear_speed"])
        if res=='back':
            self.vel_msg.linear.x=-abs(self.config["linear_speed"])

        else:
            pass

        self.vel_msg.linear.y=0
        self.vel_msg.linear.z=0
        self.vel_msg.angular.x=0
        self.vel_msg.angular.y=0
        self.vel_msg.angular.z=0

        while not rospy.is_shutdown():

            t_0=rospy.Time.now().to_sec()
            current_dist=0

            while current_dist< self.config["distance"]:

                self.pub.publish(self.vel_msg)
                t_1=rospy.Time.now().to_sec()
                current_dist=self.config["linear_speed"] *(t_1-t_0)
                self.rate.sleep()

        #stop from publishing

            self.vel_msg.linear.x=0
            self.pub.publish(self.vel_msg)

            break

    def left_right(self,res):
        """
        This function is used to move the turtlebot left and right.
        """
        direction=res
        angular_speed=self.config["angular_speed"]*3.14/180
        angle=self.config["angle"]*3.14/180
        rate=rospy.Rate(10)

        self.vel_msg.linear.y=0
        self.vel_msg.linear.z=0
        self.vel_msg.angular.x=0
        self.vel_msg.angular.y=0
        self.vel_msg.linear.x=0

        if direction=='left':
            self.vel_msg.angular.z=abs(self.config["angular_speed"])

        else:
            self.vel_msg.angular.z=-abs(self.config["angular_speed"])

        while not rospy.is_shutdown():

            t_0=rospy.Time.now().secs
            current_angle=0

            while current_angle<=angle:

                self.pub.publish(self.vel_msg)
                t_1=rospy.Time.now().secs
                current_angle=0.4*angular_speed*(t_1-t_0)
                rate.sleep()

            else:

                self.vel_msg.angular.z=0
                self.pub.publish(self.vel_msg)
                break

# EOL
