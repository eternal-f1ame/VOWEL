import os, sys
sys.path.append(os.getcwd())
from robot import Turtle_cleaner
from assets.utils import load_model

model = load_model('saved_model/gest_recog')
X = Turtle_cleaner()

# EOL