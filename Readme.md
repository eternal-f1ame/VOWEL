
# Vision-Based Gesture-Controlled Drive

## Prerequisites

### Operating System

#### Ubuntu Linux 20.04

### Text Editor: Visual Studio Code Community Version

### Mininconda

## Language

* Python >3.6.x
* Preferred 3.9

## Simulation Packages

* Gazebo

      sudo apt install gazebo

* Ros Noetic

      sudo apt install ros-noetic-desktop-full


### ROS Installation

* <a href="http://wiki.ros.org/noetic/Installation/Ubuntu">ROS Installation</a>

### Steps to Run the setup

* Clone and Fetch the Gesture Recognition repository to the folder ```/catkin_ws/src/``` as ```gesture_bot```
    > Open the terminal and Navigate to ```/catkin_ws/src/``` 

      cd catkin_ws/
    > and then enter

      catkin_make

## Python Packages

* Tensorflow
* Tensorflow Addons
* Sci-kit learn
* Pandas
* Numpy
* Imutils
* OpenCV
* ABSL
* Rospy
* Mediapipe
* Python Yaml
* Rospkg

### To install

* Steps:
    > Create a virtual environment using conda

      conda create -n ENV python=3.9
    >> Use ```ENV``` as the default env for running this entire codebase.

      conda activate ENV

    > Navigate to the python_scripts folder in your terminal and install the provided dependencies

      cd catkin_ws/src/gesture_bot/python_scripts/
      pip install -r requirements.txt

    > To finally run the setup. Navigate to the ```/catkin_ws/src``` and then

      source devel/setup.bash
      roslaunch gesture_bot drive.launch

## Pipeline Operations

* Open a terminal -> Navigate to ```HOME directory```

      cd HOME/

* Make sure a camera is connected to the system

### To train the model

* Make desired changes in model/model_specification.json and then

    > navigate to the python_scripts folder in your terminal

      cd catkin_ws/src/python_scripts
    > Train the model

      python train.py

### To run the entire pipeline

* Steps:
    > Navigate to catkin workspace

      cd catkin_ws
      source devel/setup.bash
      roslaunch gesture_bot drive.launch

    > Navigate to the python_scripts folder in a new terminal and enter

      cd HOME/catkin_ws/src/gesture_bot/python_scripts
      python main.py

* The robot and camera operations will initiallize and starting instruction messages will be provided in the terminal

### To see Tensorboard visualizations

*
    > Navigate to the python_scripts folder in your terminal

      cd ROOT_PATH 
      tensorboard --logdir EXP_PATH 
    > EXP_PATH is model checkpoints are saved eg. ```logs/DATE_TIME/train``` and ```DATE_TIME``` is the date and time when first epoch was initialized

### Changing the Hyperparameters of the Robot

* Steps
    > Navigate to ```catkin_ws/src/gesture_bot/python_scripts/robot.py```

* Values of variables named SPEED, ANGULAR_SPEED, DIST, ANGLE can be changed to change the respective self explanatory movements per prediction frame

### Lidar SLAM and other utilities

* Coming soon
