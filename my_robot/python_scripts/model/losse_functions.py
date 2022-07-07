"""
Loss Functions
"""
import sys
import tensorflow_addons.losses as siamese_losses
import tensorflow.keras.losses as classifier_losses

sys.path.append("../")

class LossFunction():
    """
    Loss Functions
    """
    def __init__(self,loss_type):
        self.loss_function = loss_type

    def get_classifier_loss(self):
        """
        Loss Functions
        """
        try:
            if self.loss_function == 'categorical_crossentropy':
                return classifier_losses.categorical_crossentropy
            if self.loss_function == 'mean_absolute_error':
                return classifier_losses.mean_absolute_error
            if self.loss_function == 'mean_squared_error':
                return classifier_losses.mean_squared_error
            if self.loss_function == 'sparse_categorical_crossentropy':
                return classifier_losses.sparse_categorical_crossentropy
            if self.loss_function == 'binary_crossentropy':
                return classifier_losses.binary_crossentropy
        except:
            print('Error: loss function not found')
            return sys.exit()

    def get_siamese_loss(self):
        """
        Loss Functions
        """
        try:
            if self.loss_function == 'contrastive_loss':
                return siamese_losses.contrastive_loss
            elif self.loss_function == 'triplet_hard_loss':
                return siamese_losses.triplet_hard_loss
            elif self.loss_function == 'triplet_semihard_loss':
                return siamese_losses.triplet_semihard_loss
        except:
            print('Error: loss function not found')
            return sys.exit()


# EOL
