import numpy as np
import cv2
import pickle
import imutils
import json

import tensorflow as tf
from tensorflow.python.keras.models import Sequential,Model
from tensorflow.python.keras.metrics import Accuracy
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Convolution2D,Dense,Softmax,InputLayer,MaxPool2D,Flatten,Dropout,Add,Input,Layer,add
from tensorflow.keras.activations import relu,softmax,tanh
from tensorflow.keras.losses import categorical_crossentropy,mean_absolute_error
from tensorflow.keras.losses import sparse_categorical_crossentropy,mean_squared_error,mean_squared_logarithmic_error
from tensorflow.python.keras.models import load_model

from sklearn.model_selection import train_test_split
from sklearn.metrics import pairwise
import xml.etree.ElementTree as ET

import rospy
import geometry_msgs
from geometry_msgs.msg import Twist