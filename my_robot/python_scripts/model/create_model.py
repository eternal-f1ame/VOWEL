"""
Creating base model
"""
import sys
import tensorflow_addons as tfa
import tensorflow.keras.applications as applications
import tensorflow.keras.backend as K
from tensorflow.keras.layers import Input, Dense, Flatten, Lambda, Dropout
from tensorflow.keras.models import Model
sys.path.append("../")
from model.helpers import eucledian_distance, eucledian_output_shape

def get_base(base_architecture, config, input_tensor, is_trainable=True):
    """
    This function is used to create the base model.
    """

    if base_architecture == 'VGG16':
        base_model = applications.vgg16.VGG16(
            weights='imagenet', 
            include_top=False, 
            input_shape=(config["HEIGHT"], config["WIDTH"], 3),
        )

    elif base_architecture == 'VGG19':
        base_model = applications.vgg19.VGG19(
            weights='imagenet', 
            include_top=False, 
            input_shape=(config["HEIGHT"], 
            config["WIDTH"], 3),
        )

    elif base_architecture == 'ResNet50':
        base_model = applications.resnet50.ResNet50(
            weights='imagenet', 
            include_top=False, 
            input_shape=(config["HEIGHT"], config["WIDTH"], 3),
        )

    elif base_architecture == 'InceptionV3':
        base_model = applications.inception_resnet_v2.InceptionResNetV2(
            weights='imagenet', 
            include_top=False, 
            input_shape=(config["HEIGHT"], config["WIDTH"], 3),
        )

    elif base_architecture == 'efficientnetb0':
        base_model = applications.efficientnet.EfficientNetB0(
            weights='imagenet', 
            include_top=False, 
            input_shape=(config["HEIGHT"], config["WIDTH"], 3),
        )

    # Freezing the layers of choice (Editable by the user)
    out = base_model(input_tensor)
    out.trainable = is_trainable
    return out

def get_siamese_loss(loss_type):
    """
    Loss function for siamese network
    """
    if loss_type == 'contrastive_loss':
        loss = tfa.losses.ContrastiveLoss(margin=1)
    elif loss_type == 'triplet_hard_loss':
        loss = tfa.losses.TripletHardLoss(margin=1)
    elif loss_type == 'triplet_semihard_loss':
        loss = tfa.losses.TripletSemiHardLoss(margin=1)
    return loss

def get_classifier_loss(loss_type):
    """
    Loss function for classifier network
    """
    if loss_type == 'categorical_crossentropy':
        loss = 'categorical_crossentropy'
    elif loss_type == 'mse':
        loss = 'mse'
    return loss


def get_model(base_architecture, model_type, num_classes, config):
    """
    This function is used to create the model.
    """
    input_tensor = Input(shape=(config["HEIGHT"], config["WIDTH"], 3))
    base = get_base(base_architecture, config, input_tensor)

    # Defining the model tail

    if model_type == 'siamese':
        layer = Flatten()(base)
        layer = Dense(2*config["embedding_size"], activation='relu')(layer)
        layer = Dropout(0.2)(layer)
        layer = Dense(config["embedding_size"])(layer)
        out = Lambda(lambda  x: K.l2_normalize(x,axis=1))(layer)
        embedding = Model(input_tensor, out)

        input_1 = Input(shape=(config["HEIGHT"], config["WIDTH"], 3))
        input_2 = Input(shape=(config["HEIGHT"], config["WIDTH"], 3))

        embedding_1 = embedding(input_1)
        embedding_2 = embedding(input_2)

        distance = Lambda(
            eucledian_distance,
            output_shape=eucledian_output_shape)(embedding_1, embedding_2)

        model = Model([input_1, input_2], distance)

        loss = get_siamese_loss(config.loss)

    elif model_type == 'classifier':
        layer = Flatten()(base)
        layer = Dense(config["embedding_size"], activation='relu')(layer)
        layer = Dropout(0.4)(layer)
        out = Dense(num_classes,activation='softmax')(layer)

        loss = get_classifier_loss(config["loss"])
        model = Model(input_tensor, out)

    model.compile(loss=loss, optimizer='adam', metrics=['accuracy'])
    return model

# EOL
