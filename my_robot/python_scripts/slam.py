import os, sys
sys.path.append(os.getcwd())
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from assets.utils import rospy, Pose, Odometry

def callback(msg):
    print(msg.pose)

rospy.init_node('check_odometry')
odom_sub = rospy.Subscriber('/odom', Odometry, callback)
rospy.spin()

# EOL