import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--platform",required=True,help="Device platform. jetbot | mac" )
parser.add_argument("--modelpath",required=True,help="keras weight(h5) file path")
parser.add_argument("--image1",required=True,help="base image path")
parser.add_argument("--image2",required=False,help="if specified, use this image instead of cam")
args = parser.parse_args()
import os
if args.platform == 'jetbot' :
  os.environ['OPENBLAS_CORETYPE'] = 'ARMV8'
from PIL import Image
import cv2
import numpy as np
import face_recognition

def infer(model,ndarray):
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

def dist(vA, vB):
  return np.sum(np.square(np.subtract(vA,vB)),1)

def encode_image_from_file(impath):
    image = Image.open(impath).convert('RGB')
    image = image.resize((112,112))
    image_np = np.asarray(image)
    image_np = np.expand_dims(image_np,0)
    image_np = (image_np - 127.5) * 0.0078125
    vec = model(image_np)
    return vec
#iu_base = encode_image_from_file('/home/jetbot/Picture/IU_1.jpg')
#iu_base2 = encode_image_from_file('/home/jetbot/Picture/IU_2.jpg')

#print(cos_sim(iu_base,iu_base2))

def crop_face_from_nd(ndarray):
  image = ndarray
  face_locations = face_recognition.face_locations(image, model="hog")
  return [ image[top:bottom, left:right] for top,right,bottom,left in face_locations  ]

def crop_face_from_file(impath):
  image = Image.open(impath).convert('RGB')
  image = np.asarray(image)
  return crop_face_from_nd(image)


def recog_step(camera_value):
    current_frame = np.copy(camera_value)
    face_locations = face_recognition.face_locations(current_frame, model="hog")
    if len(face_locations) > 0 :
        for face_coord in face_locations:
            top, right, bottom, left = face_coord
            croped_current_frame= current_frame[top:bottom, left:right]
            croped_current_frame = croped_current_frame[:,:,::-1]
            temp = croped_current_frame
            v1 = infer(croped_current_frame)
            v2 = iu_base
            sim = cos_sim(v1,v2)
            print("Sim : ",sim)   

import time
if __name__ == "__main__" :
  import tensorflow as tf
  print("Loading model from ",args.modelpath)
  model = tf.keras.models.load_model(args.modelpath)
  print("Loading done.")
  print("Embedding image 1: ",args.image1)
  croped_face_nd = crop_face_from_file(args.image1)[0]
  base1_embedding = infer(model,croped_face_nd)
  if args.image2 is not None :
    print("Embedding image 2: ",args.image2)
    croped_face_nd2 = crop_face_from_file(args.image2)[0]
    base2_embedding = infer(model,croped_face_nd2)

    #cv2.imshow('a',croped_face_nd)
    #cv2.imshow('b',croped_face_nd2)
    #cv2.waitKey(0)   #wait for a keyboard input
    #cv2.destroyAllWindows()
    
    
  #print("Embedded 128-dim vec : ",base1_embedding)
#  cv2.imwrite('croped_face.jpg',cv2.cvtColor(croped_face_nd, cv2.COLOR_RGB2BGR))
  else : #Use cam
    print("Using cam")
    if args.platform == 'jetbot' :
      from jetbot import Camera
      camera = Camera.instance(width=224, height=224)
      camera.start()
      image = np.copy(camera.value)
      camera.stop()

      croped_face_nd2 = crop_face_from_nd(image)
      base2_embedding = infer(model,croped_face_nd2)

  print("Cosine simillarity : ",cos_sim(base1_embedding, base2_embedding))
  print("Distance : ",	  dist(base1_embedding, base2_embedding))


#while True:
#    recog_step(camera.value)
#    time.sleep(0.3)
