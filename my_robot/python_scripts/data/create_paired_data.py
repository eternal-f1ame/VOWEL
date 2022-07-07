import os, sys
sys.path.append(os.getcwd())
from assets.utils import np, tf, random, shutil, time, imutils, cv2, json, Process

DIR = 'data'

class Pair(object):
    def __init__(self,data):
        x, y = data
        self.x, self.y = np.array(x), np.array(y)

    def decode_img(self, img):
        img = tf.image.decode_jpeg(img, channels=3)
        img = tf.image.convert_image_dtype(img, tf.float32)
        return img

    def get_pairs(self):
        x, y = self.x, self.y
        pairs, labels = self.makePairs(len(np.unique(y)))
        element_1, element_2 = tf.data.Dataset.from_tensor_slices(pairs[:, 0]), tf.data.Dataset.from_tensor_slices(pairs[:, 1])
        labels = tf.data.Dataset.from_tensor_slices(labels)
        return (element_1, element_2, labels)

    def makePairs(self, num_classes):
        num_classes = num_classes
        x, y = self.x, self.y
        digit_indices = [np.where(y == i)[0] for i in range(num_classes)]

        pairs = list()
        labels = list()

        for idx1 in range(len(x)):
            x1 = x[idx1]
            label1 = y[idx1]
            idx2 = random.choice(digit_indices[label1])
            x2 = x[idx2]
            
            labels += list([1])
            pairs += [[x1, x2]]

            label2 = random.randint(0, num_classes-1)
            while label2 == label1:
                label2 = random.randint(0, num_classes-1)

            idx2 = random.choice(digit_indices[label2])
            x2 = x[idx2]
            
            labels += list([0])
            pairs += [[x1, x2]]
        
        return np.array(pairs), np.array(labels)

class Augment(object):

    def rotate_img(img):
        img = tf.keras.layers.RandomRotation(0.2)(img)
        return img
    
    def zoom_img(img):
        img = tf.keras.layers.RandomZoom(0.5)(img)
        return img

    def shift_img(img):
        img = tf.keras.layers.RandomShift(0.5)(img)
        return img

    def flip_img(img):
        img = tf.keras.layers.RandomFlip()(img)
        return img

    def shear_img(img):
        img = tf.keras.preprocessing.image.random_shear(img, 0.2)
        return img

