"""
Training the model
"""
import json
from datetime import datetime
import tensorflow as tf
from model.create_model import get_model
from data.dataset_generator import generate_data_for_classifier
from tensorflow.keras.callbacks import CSVLogger


CONFIG_FILE = 'configurations.json'

with open(CONFIG_FILE, encoding="utf-8") as load_value:
    configurations = json.load(load_value)

with open(configurations["MODEL_DIR"] +
"/" + "model_specifications.json", encoding="utf-8") as specs:
    model_config = json.load(specs)

with open(configurations["DATA_DIR"] +
"/" + "augment.json", encoding="utf-8") as aug:
    aug_config = json.load(aug)

def main(_args):
    """
    Main Function
    """

    # Loading the Data
    data = generate_data_for_classifier(
        configurations["DATA_DIR"],
        model_config["batch_size"],
        target_size=(128, 128),
        augmentation_config=aug_config
        )

    # Creating the Model
    model = get_model(
        model_config["base_architecture"],
        model_type=model_config["model_type"],
        num_classes=6,
        config=model_config
    )

    # Defining the callbacks
    # ----------------------
    # Defining Checkpoints

    weights_dir = configurations["MODEL_DIR"] + "/weights"
    checkpoint = tf.keras.callbacks.ModelCheckpoint(
        weights_dir + "/" + model_config["base_architecture"] +
        model_config["model_type"] +"_"+
        model_config["loss"] +"_"+
        model_config["optimizer"] +"_"+
        str(datetime.now()) +"_"+
        "model-{epoch}-"+"_{loss:.4f}.h5",
        monitor="loss",
        verbose=1,
        save_best_only=True,
        save_weights_only=True,
        mode="min",
    )

    # Defining the Keras TensorBoard callback.
    logdir = "logs/log/" + datetime.now().strftime("%Y%m%d-%H%M%S")
    tensorboard_callback = tf.keras.callbacks.TensorBoard(
        log_dir=logdir
    )

    # Defining the CSVLogger History
    csv_log = CSVLogger(
        "logs/history/training"+"_"+
        model_config['base_architecture']+"_"+
        model_config["model_type"] +"_"+
        model_config["loss"] +"_"+
        model_config["optimizer"] +"_"+
        f"{model_config['']}"+
        ".log"
    )

    # Training the model
    with tf.device("/gpu:0"):

        model.fit(
            data,
            epochs=model_config["epochs"],
            callbacks=[tensorboard_callback, checkpoint, csv_log],
            verbose=1
        )

if __name__ == "__main__":
    try:
        tf.compat.v1.app.run(main)
    except SystemExit:
        pass

# EOL
