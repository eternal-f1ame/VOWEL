#!/usr/bin/env python
# license removed for brevity
from cmath import pi
import rospy
from std_msgs.msg import Float64


def talker():
    """
    This function is used to move Joints
    """
    pub1 = rospy.Publisher(
        '/seven_dof_arm/joint1_position_controller/command', Float64, queue_size=10)
    pub2 = rospy.Publisher(
        '/seven_dof_arm/joint2_position_controller/command', Float64, queue_size=10)
    pub3 = rospy.Publisher(
        '/seven_dof_arm/joint3_position_controller/command', Float64, queue_size=10)
    pub4 = rospy.Publisher(
        '/seven_dof_arm/joint4_position_controller/command', Float64, queue_size=10)
    pub5 = rospy.Publisher(
        '/seven_dof_arm/joint5_position_controller/command', Float64, queue_size=10)
    pub6 = rospy.Publisher(
        '/seven_dof_arm/joint6_position_controller/command', Float64, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10)  # 10hz
    shoulder_pan = int(input("Enter the shoulder pan rotation in degree:"))
    shoulder_pitch = int(input("Enter the shoulder pitch rotation in degree:"))
    elbow_roll = int(input("Enter the elbow roll rotation in degree:"))
    elbow_pitch = int(input("Enter the elbow pitch rotation in degree:"))
    wrist_roll = int(input("Enter the wrist roll rotation in degree:"))
    wrist_pitch = int(input("Enter the wrist pitch rotation in degree:"))

    while not rospy.is_shutdown():

        pub1.publish(shoulder_pan * pi/180)
        pub2.publish(shoulder_pitch*pi/180)
        pub3.publish(elbow_roll*pi/180)
        pub4.publish(elbow_pitch*pi/180)
        pub5.publish(wrist_roll*pi/180)
        pub6.publish(wrist_pitch*pi/180)
        rate.sleep()


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
