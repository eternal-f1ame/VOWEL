
# Vision-Based Gesture-Controlled Drive

## Prerequisites

### Operating System

#### Ubuntu Linux 20.04

### Text Editor: Visual Studio Code Community Version

## Language

* Python >3.6.x
* Preferred 3.8.1

## Simulation Packages

* Ros Noetoc

<code>sudo apt install ros-noetic-desktop-full</code>

* Gazebo

<code>sudo apt install gazebo</code>

## Python Packages

* Rospy
<code>pip install rospy</code>

* Tensorflow
<code>pip install tensorflow=2.80</code>

* OpenCV
<code>pip install opencv-python=4.5.5</code>

* Sklearn
<code>pip install sklearn</code>

### ROS Installation

* <a href="http://wiki.ros.org/noetic/Installation/Ubuntu">ROS Installation</a>

<h1> Steps to Run the setup</h1>

* Clone and Fetch the Gesture Recognition repository to the folder <code>/catkin_ws/src</code>

* Pull the my_robot folder out of the Gesture_Recognition folder directly into the src.

* Delete the <code>cmakelists</code> and <code>package.xml</code> from the my_robot folder.
* Open the terminal and Navigate to <code>/catkin_ws/src</code> and then enter
```
catkin make my_robot
```
* To finally run the setup. Navigate to the <code>/catkin_ws/src</code> and then
```
roslaunch my_robot drive.launch
```

* Open a text editor -> Navigate to <code>catkin_ws/src/my_robot/python_scripts/main.py</code>.
* Connect the camera and run <code>main.py</code>.
* The region Infront of the camera should have the working background present infront of it and no foreign object should enter the camera region until the message "you are good to go" is displayed in the Terminal.
