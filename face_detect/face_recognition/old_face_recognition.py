import tensorflow as tf
from PIL import Image
import numpy as np

model = tf.keras.models.load_model("/home/jetbot/keras_mobilenet_emore_adamw_5e5_soft_baseline_before_arc_E80_BTO_E2_arc_sgdw_basic_agedb_30_epoch_119_0.959333.h5")

def infer(impath):
  image = Image.open(impath).convert('RGB')
  image = image.resize((112,112))
  image_np = np.asarray(image)
  image_np = np.expand_dims(image_np,0)
  image_np = (image_np - 127.5) * 0.0078125
  return model(image_np)

def cos_sim(vA,vB):
  vA = np.squeeze(vA)
  vB = np.squeeze(vB)
  return np.dot(vA, vB) / (np.sqrt(np.dot(vA,vA)) * np.sqrt(np.dot(vB,vB)))

vec1 = infer('/home/jetbot/Picture/IU_1.jpg')
vec2 = infer('/home/jetbot/Picture/IU_2.jpg')
cos_sim(vec1,vec2)