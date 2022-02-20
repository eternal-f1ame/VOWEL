# Vision-Based Gesture-Controlled Drive

# Input Origination

Task one of using hand gestures as controls was taking the inputs ( hand-gestures ) in a proper manner wherein it can be further converted into executable commmands for the robot.

For using hand gestures as inputs, firstly I made use of the opencv-python Libriary and the rest of the codes were writen in the same language as well:

### Process: -

The frames from the webcam of my Laptop were continuously read by the python program where I performed background substraction on the hand while recording gestures.

The **first step** to background substraction was reading the background which was done performing the time weighted average of the initial 50 frames tha the webcam read. And a region of interest was set to read the hand gestures.

**Step two** of this process was the inception of a foreign object inside this background (eg. hand) as soon as the hand entered our set region of interest, A gaussian blur was performed on the readed frame to eliminate any kind of noise that might have crept into the camera readings.

A matrix substraction was performed with the pixel values of the readed background and the live frames coming in. Intutively there was supposed to be an appreciable difference between the pixel values of the region in roi where hand was present and the set background where there was no hand and after taking the absolute values from the performed matrix substraction we got two regions of pixel values, one with appreciable magnitude ( hand present regions ) other with negligible magnitude ( hand absent ).

**Next step** was performing thresholding on the final frame we have after the previous step a certain magnitude of pixel value suiting our need is set as threshold and all the pixels above that are topped up to 255 and all the pixels below it were capped to 0 giving us an image which looks like:-

![Frame0.jpg](Vision-Bas%207ea3a/Frame0.jpg)

![Frame0.jpg](Vision-Bas%207ea3a/Frame0%201.jpg)

Performing the above step gave us contour like image, which to begin with can have more than one contour, to deal with it, we measured the contour area and except for the contour with biggest area others were again capped to a pixel value of zero to finally obtain the balck and white image which can be seen above.

### Creating Dataset :-

For starters I took 5 different categories of hand gestures ( namely: front, back, right, left, stop ) nomenclature done according to the final motions which the inception of a particular hand gesture would render.

The thresholded black and whote image along with the original frames captured were stored in different folders to create a dataset which we can use in training our machine learning model.

### Machine Learning Model :-

The created directory of images ( resized images (128x128) and (256x256) ) done to simply because of my limited computational resources, was further made into a dataset of pixel values (as features ) where the labels were the categories of the hand gestures( aforementioned ).

   

![Screenshot from 2022-02-17 13-06-38.png](Vision-Bas%207ea3a/Screenshot_from_2022-02-17_13-06-38.png)

For starters a simple CNN architecture was trained on this data and validation/test accuracy of about 70 % was recieved, furthermore after training some sophisticated architectures like resnet50v2 and InceptionNet I found in both the cases the accuracy if the model was capped at 80%, hence deducing that the dataset we have is not good enough, 

- It does not have too many training samples
- It has hand-gestures only from one person( me )
- To make it workable on available computational resources the quality of images were reduced which are also a cause of limiting the versatility of the data.

Nonetheless the model was trained and the weights were saved:-  

![Screenshot from 2022-02-17 13-19-02.png](Vision-Bas%207ea3a/Screenshot_from_2022-02-17_13-19-02.png)

![Screenshot from 2022-02-17 13-18-40.png](Vision-Bas%207ea3a/Screenshot_from_2022-02-17_13-18-40.png)

# Output Generation:-

### `Video()` function

A function in python programming language was created which after performing background subtraction and segmentation on the live frames beig inputted in the program through webcam predicts results on one in every **n** images, this is done so to perform the prediction and capture frames in real time smoothly.

![Screenshot from 2022-02-17 13-29-00.png](Vision-Bas%207ea3a/Screenshot_from_2022-02-17_13-29-00.png)

*A snippet of a part of the code of `video()` function is provided above*.

### Prediction

After the video function facilitates the thresholded black and white hand contour image, the image is scaled to the same size as the input images in the ML model were and passed through the saved model to get on of the predicted classes in return.

`video()` function contains a dictionary that has keys corresponding to the outputs from the saved ml model the key value pairs in the same dictionary are label and its executable command respectively().

# Gesture-Controlled Bot

### Driving the Robot

The executable command which is obtained from the `Video()` function is used to call rospy functions in a `turtle cleaner` class which is responsible for the movement of the robot in gazebo simulation.

### Basic Info

The Gesture Following Bot is made using the combination of ROS, Gazebo, and AI.

It integrates all the different features of a robot and builds a connection between them through the concept of nodes and messages. The gazebo is the most widely used robotics simulation platform. On Gazebo it is possible to test algorithms, design robots and check their working in various physical conditions. 
It uses urdf file format to define the robots in the simulation.

![Screenshot from 2022-02-17 13-53-51.png](Vision-Bas%207ea3a/Screenshot_from_2022-02-17_13-53-51.png)

### Features and Parts

The gesture following bot has 1 base link to which other components are attached, 4 wheels, 1 rod to which a rotating cylinder is attached. These are the basic components of the robot and the total mass of the robot is 4.5 kg. 

The wheels are controlled using ROS controllers like differential drive controllers, especially for wheels. Through these controllers, the angular velocities and linear velocities of each wheel can be controlled for smooth movements of the robot. 

These controllers are stored in the config folder in Yaml file format. Using Ros and gazebo various sensors like cameras and lidars can be easily attached to the robot. In this gesture following bot there are two sensors attached to the robot one is the camera which is attached on the top cylinder to detect obstacles and objects. 

![Screenshot from 2022-02-17 13-55-33.png](Vision-Bas%207ea3a/Screenshot_from_2022-02-17_13-55-33.png)

![Screenshot from 2022-02-17 13-53-06.png](Vision-Bas%207ea3a/Screenshot_from_2022-02-17_13-53-06.png)

### Extras

Another sensor is a lidar sensor which can determine the distance of obstacles from the robot for any further operations.