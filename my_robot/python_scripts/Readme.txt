Requirements:
    Python 3.9
    Miniconda
To set up the Environment follow the instructions below
    - >>conda create -n gesture_env python=3.9
    - >>conda activate gesture_env
    - >>cd ROOT_PATH //(navigate to the python_scripts folder in your terminal)
    - >>pip install -r requirements.txt //(installing all the dependencies)

    The environment is set

To train the model
    Make desired changes in model/model_specification.json
    - >>cd ROOT_PATH //(navigate to the python_scripts folder in your terminal)
    - >>python train.py

To run the entire pipeline
    - >>cd catkin_ws //(Navigate to catkin workspace)
    - >>source devel/setup.bash
    - >>roslaunch my_robot drive.launch

    - >>cd ROOT_PATH //(navigate to the python_scripts folder in a new terminal)
    - >>python main.py

To see tensorboard visualizations
    - >>cd ROOT_PATH //(navigate to the python_scripts folder in your terminal)
    - >>tensorboard --logdir EXP_PATH //(path where checkpoints are saved eg. logs/DATE_TIME/train)