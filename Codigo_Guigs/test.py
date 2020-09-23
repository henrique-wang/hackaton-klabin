import os
import numpy as np
from PIL import Image
import cv2


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dataset_dir = os.path.join(BASE_DIR,'dataset')

xtrain=[]
ylabel=[]

detector = cv2.CascadeClassifier("Cascades\haarcascade_frontalface_default.xml");

#Let's grab all the photos from our dataset to train
for root, dirs, files in os.walk(dataset_dir):
    for file in files:
        if file.endswith('png') or file.endswith('jpg'):
            path=os.path.join(root, file)
            label=os.path.basename(os.path.dirname(path))
            print(label, path)
            #Let's treat the image
            pil_image = Image.open(path).convert('L')
            image_array = np.array(pil_image, 'uint8')
            print(image_array)
            faces = detector.detectMultiScale(image_array)
            for (x, y, w, h) in faces:
                roi=image_array[y:y + h, x:x + w]
                xtrain.append(roi)
                ylabel.append(int(label))
print(ylabel)
