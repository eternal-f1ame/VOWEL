"""
Main Function
"""
import json
import sys
# from multiprocessing import Process
from threading import Thread as Process
import rospy
from robot import TurtleCleaner
from video import live, move
# from deprecated_video import video

#!/usr/bin/env python

if __name__ == '__main__':
    try:
        robot_config = json.load(open(
            'robot_configurations.json',
            encoding="utf-8"))
        print("""
        Welcome to the Turtle Cleaner Robot



        """)
        print(robot_config)

        # Initializing the robot
        Bot = TurtleCleaner(robot_config=robot_config)

        # Initializing the threads
        #-------------------------

        # video_thread : Bot Movement Control
        p1 = Process(target=move, args=[Bot])
        p1.start()

        # video_thread : Hand Gesture Recognition
        p2 = Process(target=live)
        if not p1.is_alive():
            p1.start()
        if not p2.is_alive():
            p2.start()
        p1.join()
        p2.join()
    except rospy.ROSInterruptException:
        sys.exit()

    except KeyboardInterrupt:
        sys.exit()

# EOL
