from utils import *
from count_fingers import *
from predict import *
from run_avg import *
from segment import *
from global_vars import *
import tensorflow as tf
from PIL import im
MODEL=None

def load_model(directory,isTF=True):
    if isTF:
        MODEL=tf.keras.models.load_model(directory)
    else:
        MODEL=torch.load(directory)

def evaluate(test_images,test_labels):
    loss, acc = MODEL.evaluate(test_images, test_labels, verbose=2)
    print('accuracy: {:5.2f}%'.format(100 * acc))

def get_bounding_box(frame,predictions):
    pass

def predict(frame,target_sz):
    FrameClone=frame.copy()
    img=tf.keras.utils.load_img(FrameClone,target_size=target_sz)
    img=tf.keras.utils.img_to_array(img)
    img=img.astype('float32')
    img/=255
    img=tf.keras.utils.expand_dims(img,0)
    predictions=MODEL.predict(img)
    
if __name__ == "__main__":

    
    camera = cv2.VideoCapture(0)

    
    num_frames = 0

    
    while(True):

        (grabbed, frame) = camera.read()

        #frame = imutils.resize(frame, width=700)

        frame = cv2.flip(frame, 1)

        clone = frame.copy()

        (height, width) = frame.shape[:2]

       
        denoised = cv2.GaussianBlur(clone, (7, 7), 0)

            
    
        num_frames += 1

        cv2.imshow("Video Feed", clone)
        
        keypress = cv2.waitKey(1) & 0xFF

        if num_frames == 100000:

            break



