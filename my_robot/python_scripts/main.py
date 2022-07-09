"""
Main Function
"""
import sys
import json
sys.path.append("../")
from deprecated_video import video
from video import hands_live
#!/usr/bin/env python
from robot import TurtleCleaner
import rospy

if __name__ == '__main__':
    try:
        robot_config = json.load(open(
            'robot_configurations.json',
            encoding="utf-8"))
        print("""
        Welcome to the Turtle Cleaner Robot



        """)
        print(robot_config)
        Bot = TurtleCleaner(robot_config=robot_config)
        hands_live(Bot)

    except rospy.ROSInterruptException:
        pass

# EOL