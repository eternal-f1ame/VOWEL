"""
Training the model
"""
import json
from datetime import datetime
import tensorflow as tf
from model.create_model import get_model
from data.dataset_generator import generate_data_for_classifier


CONFIG_FILE = 'configurations.json'

with open(CONFIG_FILE, encoding="utf-8") as load_value:
    configurations = json.load(load_value)

print(configurations)
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


    # Loading the model

    weights_dir = f'{configurations["MODEL_DIR"]}'+'/weights'
    model = get_model(
        model_config["base_architecture"],
        model_type='classifier',
        num_classes=6,
        config=model_config)
    checkpoint = tf.keras.callbacks.ModelCheckpoint(
        weights_dir + "/" + model_config["base_architecture"] +
        "model-{epoch}-"+"_{loss:.4f}.h5",
        monitor="loss",
        verbose=1,
        save_best_only=True,
        save_weights_only=True,
        mode="min",
    )

    # Defining the Keras TensorBoard callback.
    logdir = "logs/fit/" + datetime.now().strftime("%Y%m%d-%H%M%S")
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=logdir)
    print(data)

    with tf.device("/gpu:0"):

        history = model.fit(
            data,
            epochs=model_config["epochs"],
            callbacks=[tensorboard_callback, checkpoint],
            verbose=1
        )
    history.save("history" + "/" + model_config["base_architecture"])

if __name__ == "__main__":
    try:
        tf.compat.v1.app.run(main)

    except SystemExit:
        pass


# EOL
