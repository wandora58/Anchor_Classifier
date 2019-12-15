import base64
import io
import os.path

import cv2
import numpy as np
import tensorflow as tf
from PIL import Image
from django.db import models
from keras.models import load_model
from stdimage.models import StdImageField

graph = tf.get_default_graph()


class Photo(models.Model):
    image = StdImageField(upload_to='img/', blank=True, variations={
        'resize': (300, 200)
    })

    CURRENT_DIR = os.getcwd()
    MODEL_FILE_PATH = CURRENT_DIR + '/anchor/ml_models/aianchor_simple.h5'

    classes = ["Asahi", "Fuji", "Japan", "NHK", "TBS"]
    num_classes = len(classes)

    def predict(self):

        model = None

        global graph
        with graph.as_default():

            model = load_model(self.MODEL_FILE_PATH)

            img_data = self.image.read()
            img_bin = io.BytesIO(img_data)
            img_pil = Image.open(img_bin)
            img_numpy = np.asarray(img_pil)
            img_numpy_bgr = cv2.cvtColor(img_numpy, cv2.COLOR_RGBA2BGR)

            CURRENT_DIR = os.getcwd()
            face_cascade_path = CURRENT_DIR + '/anchor/opencv/haarcascade_frontalface_default.xml'
            face_cascade = cv2.CascadeClassifier(face_cascade_path)

            faces = face_cascade.detectMultiScale(img_numpy_bgr)

            if len(faces) > 0:
                for rect in faces:
                    x = rect[0]
                    y = rect[1]
                    width = rect[2]
                    height = rect[3]
                    img = img_numpy_bgr[y:y + height, x:x + width]

            else:
                return None, 0

            IMAGE_SIZE = 100

            data = cv2.resize(img, (IMAGE_SIZE, IMAGE_SIZE))
            data = np.array(data) / 255.0
            X = []
            X.append(data)
            X = np.array(X)

            result = model.predict([X])[0]
            predicted = result.argmax()

            return result, self.classes[predicted]

    def image_src(self):
        with self.image.open() as img:
            base64_img = base64.b64encode(img.read()).decode()

            return 'data:' + img.file.content_type + ';base64,' + base64_img
