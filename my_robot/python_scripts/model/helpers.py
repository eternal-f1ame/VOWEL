import os, sys
sys.path.append(os.getcwd())

from assets.utils import *

# metrics

def eucledian_distance(x, y):
    squared_sum =  K.sqrt(K.sum(K.square(x - y)), axis=1, keep_dims=True)
    distance = K.sqrt(K.maximum(squared_sum, K.epsilon()))
    return distance

def eucledian_output_shape(x, y):
    assert x.shape[0] == y.shape[0], "embedding sizes must be equal"
    return (x.shape[0], 1)

def accuracy(y_original, y_pred, threshold=0.5):
    return K.mean(K.equal(y_original, K.cast(y_pred < threshold, y_original.dtype)))


# pairs

class Pair(object):
    def __init__(self,data):
        self.x, self.y = data

    def get_pairs(self, Imge_generator):
        x, y = self.x, self.y
        pairs, labels = self.makePairs(len(np.unique(y)))
        return ImageDataGenerator.flow(pairs, labels, )

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


# EOL