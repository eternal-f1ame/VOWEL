import os, sys
sys.path.append(os.getcwd())
from assets.utils import ImageDataGenerator, tf
from model.helpers import Pair
from data.create_paired_data import Pair, Augment

def generate_data_for_classifier(DATA_DIR, batch_size, target_size, augmentation_config):

    # DATA_DIR = 'data'
    IMAGE_DIR = f'{DATA_DIR}/gestures'

    image_generator = ImageDataGenerator(
        rescale=1./255,
        rotation_range=augmentation_config['rotation_range'],
        width_shift_range=augmentation_config['width_shift_range'],
        height_shift_range=augmentation_config['height_shift_range'],
        shear_range=augmentation_config['shear_range'],
        zoom_range=augmentation_config['zoom_range'],
        horizontal_flip=augmentation_config['horizontal_flip'],
        )
    image_data = image_generator.flow_from_directory(
        IMAGE_DIR,
        target_size=target_size,
        batch_size=batch_size,
        class_mode='categorical',
    )

    return image_data

def generate_data_for_siamese(DATA_DIR = "C:\\Users\\aeternum\\Documents\\GitHub\\Gesture-Recognition\\my_robot\\python_scripts\\data"):

    # DATA_DIR = 'data'
    IMAGE_DIR = f'{DATA_DIR}\\gestures'

    images = []
    labels = []

    # Map paths to images

    def augment_pairs(image_data_1,image_data_2,labels,augmentation_config):

        augmented_image_data_1 = image_data_1
        augmented_image_data_2 = image_data_2
        augmented_labels = labels

        if "rotation_range" in augmentation_config:
            rotated_1 = image_data_1.map(Augment.rotate_img)
            rotated_2 = image_data_2.map(Augment.rotate_img)

            augmented_image_data_1 = augmented_image_data_1.concatenate(rotated_1)
            augmented_image_data_2 = augmented_image_data_2.concatenate(rotated_2)
            augmented_labels = augmented_labels.concatenate(labels)

        if "width_shift_range" in augmentation_config:
            w_shifted_1 = image_data_1.map(Augment.shift_img)
            w_shifted_2 = image_data_2.map(Augment.shift_img)

            augmented_image_data_1 = augmented_image_data_1.concatenate(w_shifted_1)
            augmented_image_data_2 = augmented_image_data_2.concatenate(w_shifted_2)
            augmented_labels = augmented_labels.concatenate(labels)

        if "height_shift_range" in augmentation_config:
            h_shifted_1 = image_data_1.map(Augment.shift_img)
            h_shifted_2 = image_data_2.map(Augment.shift_img)

            augmented_image_data_1 = augmented_image_data_1.concatenate(h_shifted_1)
            augmented_image_data_2 = augmented_image_data_2.concatenate(h_shifted_2)
            augmented_labels = augmented_labels.concatenate(labels)

        if "zoom_range" in augmentation_config:
            zoomed_1 = image_data_1.map(Augment.zoom_img)
            zoomed_2 = image_data_2.map(Augment.zoom_img)

            augmented_image_data_1 = augmented_image_data_1.concatenate(zoomed_1)
            augmented_image_data_2 = augmented_image_data_2.concatenate(zoomed_2)
            augmented_labels = augmented_labels.concatenate(labels)

        if "flip_horizontal" in augmentation_config:
            flipped_1 = image_data_1.map(Augment.flip_img)
            flipped_2 = image_data_2.map(Augment.flip_img)

            augmented_image_data_1 = augmented_image_data_1.concatenate(flipped_1)
            augmented_image_data_2 = augmented_image_data_2.concatenate(flipped_2)
            augmented_labels = augmented_labels.concatenate(labels)

        if "shear_range" in augmentation_config:
            sheared_1 = image_data_1.map(Augment.shear_img)
            sheared_2 = image_data_2.map(Augment.shear_img)

            augmented_image_data_1 = augmented_image_data_1.concatenate(sheared_1)
            augmented_image_data_2 = augmented_image_data_2.concatenate(sheared_2)
            augmented_labels = augmented_labels.concatenate(labels)

        return (augmented_image_data_1,augmented_image_data_2,augmented_labels)


    def decode_img(img):
        img = tf.io.read_file(img)
        img = tf.image.decode_jpeg(img, channels=3)
        img = tf.image.resize(img, (224, 224))
        # img = tf.image.convert_image_dtype(img, tf.float32)
        return img

    
    for folder in os.listdir(IMAGE_DIR):
        for image in os.listdir(f'{IMAGE_DIR}/{folder}'):
            images.append(f'{IMAGE_DIR}/{folder}/{image}')
            labels.append(int(folder))

    pair_generator = Pair((images, labels))
    element_set_1, element_set_2, pair_labels =  pair_generator.get_pairs()

    # Evaluate the dataset

    element_set_1 = element_set_1.map(decode_img)
    element_set_2 = element_set_2.map(decode_img)
    pair_labels = pair_labels.map(lambda x: tf.one_hot(x, 2))

    return (element_set_1, element_set_2, pair_labels)
    


# EOL