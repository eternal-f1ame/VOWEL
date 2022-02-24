import tensorflow as tf
from tensorflow.keras.models import Sequential,Model
from tensorflow.keras.metrics import Accuracy
from tensorflow.keras.optimizers import Adam,SGD
from tensorflow.keras.layers import Convolution2D,Dense,Softmax,InputLayer,MaxPool2D,Flatten,Dropout,Add,Input,Layer,add
from tensorflow.keras.activations import relu,softmax,tanh
from tensorflow.keras.losses import categorical_crossentropy,mean_absolute_error
from tensorflow.keras.losses import sparse_categorical_crossentropy,mean_squared_error,mean_squared_logarithmic_error
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import cv2
from tensorflow import convert_to_tensor
from sklearn.preprocessing import LabelEncoder
import pickle
le = LabelEncoder()
import imutils
import numpy as np
from sklearn.metrics import pairwise
from sklearn.cluster import k_means
from tensorflow.keras.models import load_model
from tensorflow import convert_to_tensor
import xml.etree.ElementTree as ET

