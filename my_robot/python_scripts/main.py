"""
Main Function
"""
import sys
import json
sys.path.append("../")
from video import video
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
        video(Bot)

    except rospy.ROSInterruptException:
        pass

# EOL