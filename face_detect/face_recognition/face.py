import os
os.environ['OPENBLAS_CORETYPE'] = 'ARMV8'
from jetbot import Camera
import tensorflow as tf
from PIL import Image
import numpy as np

def infer(ndarray):
  image = Image.fromarray(ndarray)
  image = image.resize((112,112))
  image_np = np.asarray(image)
  image_np = np.expand_dims(image_np,0)
  image_np = (image_np - 127.5) * 0.0078125
  return model(image_np)

def cos_sim(vA,vB):
  vA = np.squeeze(vA)
  vB = np.squeeze(vB)
  return np.dot(vA, vB) / (np.sqrt(np.dot(vA,vA)) * np.sqrt(np.dot(vB,vB)))


model = tf.keras.models.load_model("keras_se_mobile_facenet_emore_triplet_basic_agedb_30_epoch_100_0.958333.h5")
camera = Camera.instance(width=224, height=224)

def encode_image_from_file(impath):
    image = Image.open(impath).convert('RGB')
    image = image.resize((112,112))
    image_np = np.asarray(image)
    image_np = np.expand_dims(image_np,0)
    image_np = (image_np - 127.5) * 0.0078125
    vec = model(image_np)
    return vec
iu_base = encode_image_from_file('/home/jetbot/Picture/IU_1.jpg')
iu_base2 = encode_image_from_file('/home/jetbot/Picture/IU_2.jpg')

print(cos_sim(iu_base,iu_base2))

import face_recognition
temp = None
def recog_step(camera_value):
    global temp
    current_frame = np.copy(camera_value)
    #print("data copied")
    face_locations = face_recognition.face_locations(current_frame, model="hog")
    if len(face_locations) > 0 :
        #print("face detected")
        for face_coord in face_locations:
            #print("Coord : ",face_coord)
            top, right, bottom, left = face_coord
            croped_current_frame= current_frame[top:bottom, left:right]
            croped_current_frame = croped_current_frame[:,:,::-1]
            temp = croped_current_frame
            v1 = infer(croped_current_frame)
            #print("inferred")
            v2 = iu_base
            sim = cos_sim(v1,v2)
            print("Sim : ",sim)   

camera.start()
import time
while True:
    recog_step(camera.value)
    time.sleep(0.3)
