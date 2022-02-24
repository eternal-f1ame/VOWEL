from utils import *
from video import *
from robot import *

if __name__ == '__main__':
    
    try:
        x=Turtle_cleaner()
        
        video(x)

    except rospy.ROSInterruptException:
    
        pass
    