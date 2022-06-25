import os, sys
sys.path.append(os.getcwd())
from video import video
from assets.utils import json
#!/usr/bin/env python
from robot import Turtle_cleaner
import rospy

if __name__ == '__main__':
    try:
        robot_config = json.load(open('robot_configurations.json'))
        Bot = Turtle_cleaner(robot_config=robot_config)
        video(Bot)

    except rospy.ROSInterruptException:
        pass

# EOL