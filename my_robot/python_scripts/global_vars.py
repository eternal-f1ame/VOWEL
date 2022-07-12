"""
Global Variables
"""
import sys
sys.path.append('../')
from robot import TurtleCleaner
from tensorflow.keras.models import load_model

model = load_model('model/saved/resnet_model.h5')

# EOL
