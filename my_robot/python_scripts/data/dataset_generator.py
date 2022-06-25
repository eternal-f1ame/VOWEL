import os, sys
sys.path.append(os.getcwd())
from assets.utils import ImageDataGenerator

def generate_data(batch_size, target_size, augmentation_config):

    DATA_DIR = 'data'
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

# EOL