import os, sys
sys.path.append(os.getcwd())

from assets.utils import classifier_losses, siamese_losses

class loss_function():
    def __init__(self,loss_type):
        self.loss_type = loss_type
        
    def get_classifier_loss(self,loss_function):
        if self.loss_function == 'categorical_crossentropy':
            return classifier_losses.categorical_crossentropy
        elif self.loss_function == 'mean_absolute_error':
            return classifier_losses.mean_absolute_error
        elif self.loss_function == 'mean_squared_error':
            return classifier_losses.mean_squared_error
        elif self.loss_function == 'sparse_categorical_crossentropy':
            return classifier_losses.sparse_categorical_crossentropy
        elif self.loss_function == 'binary_crossentropy':
            return classifier_losses.binary_crossentropy

    def get_siamese_loss(self,loss_function):
        if self.loss_function == 'contrastive_loss':
            return siamese_losses.contrastive_loss
        elif self.loss_function == 'triplet_hard_loss':
            return siamese_losses.triplet_hard_loss
        elif self.loss_function == 'triplet_semihard_loss':
            return siamese_losses.triplet_semihard_loss
    

# EOL

    

