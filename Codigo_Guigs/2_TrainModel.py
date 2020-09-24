import os
import numpy as np
from PIL import Image
import cv2

# Path for face image database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dataset_dir = os.path.join(BASE_DIR,'dataset')

xtrain=[]
ylabel=[]

cascade_dir = os.path.join(BASE_DIR,'cascades/haarcascade_frontalface_default.xml')
detector = cv2.CascadeClassifier(cascade_dir)

recognizer = cv2.face.LBPHFaceRecognizer_create()

# function to get the images and label data
def getImagesAndLabels(path):

    for root, dirs, files in os.walk(path):
        for file in files:
            #Let's find the images
            if file.endswith('png') or file.endswith('jpg'):
                path = os.path.join(root, file)
                label = os.path.basename(os.path.dirname(path))

                # Let's treat the image
                pil_image = Image.open(path).convert('L')
                image_array = np.array(pil_image, 'uint8')

                # Let's find the faces
                faces = detector.detectMultiScale(image_array)
                for (x, y, w, h) in faces:
                    roi = image_array[y:y + h, x:x + w]
                    xtrain.append(roi)
                    ylabel.append(int(label))
    # Let's return the converted images and the respective labels
    return xtrain, ylabel

def Train():

    print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
    xtrain, ylabel = getImagesAndLabels(dataset_dir)
    recognizer.train(xtrain, np.array(ylabel))
    # Save the model into trainer/trainer.yml
    trainer_dir = os.path.join(BASE_DIR, 'trainer/trainer.yml')
    if not os.path.exists(trainer_dir):
        print("Cretaing new directory")
        os.mkdir(os.path.join(BASE_DIR, 'trainer'))
    s=trainer_dir.replace('\\', '/')
    print(s)
    recognizer.write(s)
    # Print the numer of faces trained and end program
    print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ylabel))))

