"""
Robot Intializations
"""
import sys
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float64


sys.path.append("../")
#!/usr/bin/env python
# -*- coding: utf-8 -*-


class TurtleCleaner():
    """
    This function is used to move the turtlebot forward, backward, left and right.
    """

    def __init__(self, robot_config):
        #self.pub= rospy.Publisher(
        # "/seven_dof_arm/base_velocity_controller/cmd_vel", Twist,queue_size=10)
        self.sub = rospy.Subscriber("/scan", LaserScan, self.callback)
        self.pub1 = rospy.Publisher(
            '/seven_dof_arm/base_velocity_controller/cmd_vel', Twist, queue_size=10)
        self.s_pi = rospy.Publisher(
            '/seven_dof_arm/joint2_position_controller/command', Float64, queue_size=10)
        self.s_pa = rospy.Publisher(
            '/seven_dof_arm/joint1_position_controller/command', Float64, queue_size=10)
        self.e_pa=rospy.Publisher(
            '/seven_dof_arm/joint3_position_controller/command', Float64, queue_size=10)
        self.e_pi=rospy.Publisher(
            '/seven_dof_arm/joint4_position_controller/command', Float64, queue_size=10)
        self.w_pa=rospy.Publisher(
            '/seven_dof_arm/joint5_position_controller/command', Float64, queue_size=10)
        self.w_pi=rospy.Publisher(
            '/seven_dof_arm/joint6_position_controller/command', Float64, queue_size=10)

        rospy.init_node('Mining_robot', anonymous=True)
        self.vel_msg = Twist()
        self.rate = rospy.Rate(1)
        self.config = robot_config
        self.degree_s_pi = 0
        self.degree_s_pa = 0
        self.degree_e_pi = 0
        self.degree_e_pa = 0
        self.degree_w_pi = 0
        self.degree_w_pa = 0
        self.obstacle = False

    def front_back(self, res):
        """
        This function is used to move the turtlebot forward and backward.
        """
        if not self.obstacle:
            if res == 'front':
                self.vel_msg.linear.x = abs(self.config["linear_speed"])
            if res == 'back':
                self.vel_msg.linear.x = -abs(self.config["linear_speed"])

            else:
                pass

            self.vel_msg.linear.y = 0
            self.vel_msg.linear.z = 0
            self.vel_msg.angular.x = 0
            self.vel_msg.angular.y = 0
            self.vel_msg.angular.z = 0

            while not rospy.is_shutdown():
                t_0 = rospy.Time.now().to_sec()
                current_dist = 0

                while current_dist < self.config["distance"]:

                    self.pub1.publish(self.vel_msg)
                    t_1 = rospy.Time.now().to_sec()
                    current_dist = self.config["linear_speed"] * (t_1-t_0)
                    self.rate.sleep()

            # stop from publishing

                self.vel_msg.linear.x = 0
                self.pub1.publish(self.vel_msg)

                break

    def left_right(self, res):
        """
        This function is used to move the turtlebot left and right.
        """
        if not self.obstacle:
            direction = res
            angular_speed = self.config["angular_speed"]*3.14/180
            angle = self.config["angle"]*3.14/180
            rate = rospy.Rate(10)

            self.vel_msg.linear.y = 0
            self.vel_msg.linear.z = 0
            self.vel_msg.angular.x = 0
            self.vel_msg.angular.y = 0
            self.vel_msg.linear.x = 0

            if direction == 'left':
                self.vel_msg.angular.z = abs(self.config["angular_speed"])

            else:
                self.vel_msg.angular.z = -abs(self.config["angular_speed"])

            while not rospy.is_shutdown():

                t_0 = rospy.Time.now().secs
                current_angle = 0

                while current_angle <= angle:

                    self.pub1.publish(self.vel_msg)
                    t_1 = rospy.Time.now().secs
                    current_angle = 0.4*angular_speed*(t_1-t_0)
                    rate.sleep()

                self.vel_msg.angular.z = 0
                self.pub1.publish(self.vel_msg)
                break

    def action(self, res):
        """
        This function is used to move robotic arm"""
        if not self.obstacle:
            self.vel_msg.linear.y = 0
            self.vel_msg.linear.z = 0
            self.vel_msg.angular.x = 0
            self.vel_msg.angular.y = 0
            self.vel_msg.linear.x = 0
            self.vel_msg.angular.z = 0
            self.pub1.publish(self.vel_msg)

            if res == 'action_1':
                self.e_pi.publish(1.9325)
                self.e_pa.publish(-1.222)
                self.s_pa.publish(0.14317)
                self.s_pi.publish(-0.02179)
                self.w_pi.publish(1.017)
                self.w_pa.publish(0.00)

            if res == 'action_2':
                self.e_pi.publish(1.086)
                self.e_pa.publish(0.2403)
                self.s_pa.publish(0.08)
                self.s_pi.publish(0.8460)
                self.w_pi.publish(-0.1278)
                self.w_pa.publish(-0.00001)

            if res == 'action_3':
                self.e_pi.publish(0.697)
                self.e_pa.publish(0.506)
                self.s_pa.publish(0.00)
                self.s_pi.publish(0.0)
                self.w_pi.publish(0.0)
                self.w_pa.publish(0.0000)

            # if res == 'switch':
            #     if self.degree_2 > 0:
            #         self.degree_2 -= 3
            #         self.pub3.publish((self.degree_2)*pi/180)
    def take_action(self,regions):
        """
        This function is used to take action based on the detected regions.
        """
        msg = Twist()
        linear_x = 0
        angular_z = 0

        state_description = ''

        if regions['front'] > 1 and regions['fleft'] > 1 and regions['fright'] > 1:
            state_description = 'case 1 - nothing'

        elif regions['front'] < 1 and regions['fleft'] > 1 and regions['fright'] > 1:
            state_description = 'case 2 - front'
            self.obstacle = True
            linear_x = 0
            angular_z = -0.3
        elif regions['front'] > 1 and regions['fleft'] > 1 and regions['fright'] < 1:
            state_description = 'case 3 - fright'
            self.obstacle = True
            linear_x = self.config["linear_speed"]/4
            angular_z = -0.3
        elif regions['front'] > 1 and regions['fleft'] < 1 and regions['fright'] > 1:
            state_description = 'case 4 - fleft'
            self.obstacle = True
            linear_x = self.config["linear_speed"]/4
            angular_z = 0.3
        elif regions['front'] < 1 and regions['fleft'] > 1 and regions['fright'] < 1:
            state_description = 'case 5 - front and fright'
            self.obstacle = True
            linear_x = self.config["linear_speed"]/8
            angular_z = -0.3
        elif regions['front'] < 1 and regions['fleft'] < 1 and regions['fright'] > 1:
            state_description = 'case 6 - front and fleft'
            self.obstacle = True
            linear_x = self.config["linear_speed"]/8
            angular_z = 0.3
        elif regions['front'] < 1 and regions['fleft'] < 1 and regions['fright'] < 1:
            state_description = 'case 7 - front and fleft and fright'
            self.obstacle = True
            linear_x = self.config["linear_speed"]/4
            angular_z = -0.3
        # elif regions['front'] > 1 and regions['fleft'] < 1 and regions['fright'] < 1:
        #     state_description = 'case 8 - fleft and fright'
        #     self.obstacle = True
        #     linear_x = self.config["linear_speed"]/4
        #     angular_z = -0.3
        else:
            state_description = 'unknown case'
            rospy.loginfo(regions)

        rospy.loginfo(state_description)

        if self.obstacle:
            msg.linear.x = linear_x
            msg.angular.z = angular_z
            self.pub1.publish(msg)


    def callback(self,msg):
        """
        Callback function for the subscriber
        """
        regions = {
            'right':  min(min(msg.ranges[0:143]), 10),
            'fright': min(min(msg.ranges[144:287]), 10),
            'front':  min(min(msg.ranges[288:431]), 10),
            'fleft':  min(min(msg.ranges[432:575]), 10),
            'left':   min(min(msg.ranges[576:713]), 10),
        }

        self.take_action(regions)
# EOL
