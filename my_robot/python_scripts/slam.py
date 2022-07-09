"""
Slam operations
"""
import sys
import rospy
from nav_msgs.msg import Odometry
sys.path.append('../')

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from geometry_msgs.msg import Pose


def callback(msg):
    """
    This function is used to get the current position of the robot.
    """
    print(msg.pose)

rospy.init_node('check_odometry')
odom_sub = rospy.Subscriber('/odom', Odometry, callback)
rospy.spin()

# EOL
