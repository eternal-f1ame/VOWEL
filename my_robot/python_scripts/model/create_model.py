"""
Creating base model
"""
import sys
import tensorflow.keras.applications as applications
import tensorflow.keras.backend as K
from tensorflow.keras.layers import Input, Dense, Flatten, Lambda, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
sys.path.append("../")

def get_base(base_architecture, config, Input, isTrainable=True):

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

    for layer in base_model.layers:
        layer.trainable = isTrainable

    out = base_model(Input)
    return out

def get_siamese_loss(loss_type):

    pass

def get_classifier_loss(loss_type):
    if loss_type == 'categorical_crossentropy':
        loss = 'categorical_crossentropy'
    elif loss_type == 'mse':
        loss = 'mse'
    return loss


def get_model(base_architecture, model_type, num_classes, config):
    INPUT = Input(shape=(config["HEIGHT"], config["WIDTH"], 3))
    base = get_base(base_architecture, config, INPUT)

    if model_type == 'siamese':
        layer = Flatten()(base)
        layer = Dense(1024, activation='relu')(layer)
        layer = Dropout(0.2)(layer)
        # layer = Dense(512, activation='relu')(layer)
        # layer = Dropout(0.2)(layer)
        layer = Dense(config.embedding_size)(layer)
        out = Lambda(lambda  x: K.l2_normalize(x,axis=1))(layer)
        embedding = Model(INPUT, out)

        Input_1 = Input(shape=(config["HEIGHT"], config["WIDTH"], 3))
        Input_2 = Input(shape=(config["HEIGHT"], config["WIDTH"], 3))

        embedding_1 = embedding(Input_1)
        embedding_2 = embedding(Input_2)

        distance = Lambda(euclideanDistance, output_shape=eucl_dist_output_shape)(embedding_1, embedding_2)
        model = Model([Input_1, Input_2], distance)

        loss = get_siamese_loss(config.siamese_loss)

    elif model_type == 'classifier':
        layer = Flatten()(base)
        layer = Dense(1024, activation='relu')(layer)
        layer = Dropout(0.4)(layer)
        out = Dense(num_classes,activation='softmax')(layer)

        loss = get_classifier_loss(config["classifier_loss"])
        model = Model(INPUT, out)

    model.compile(loss=loss, optimizer='adam', metrics=['accuracy'])
    return model
# EOL