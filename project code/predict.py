import numpy as np
from tensorflow.keras.models import load_model
import cv2
import os
from PIL import Image, ImageChops, ImageEnhance
import itertools

model = load_model(r'/final/best_forgery_classifier1.h5') # give path of the model file 
image_size = (128, 128)

def convert_to_ela_image(path, quality):
    temp_filename = 'temp_file_name.jpg'
    ela_filename = 'temp_ela.png'
    image = Image.open(path).convert('RGB')
    image.save(temp_filename, 'JPEG', quality = quality)
    temp_image = Image.open(temp_filename)
    ela_image = ImageChops.difference(image, temp_image)
    extrema = ela_image.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    if max_diff == 0:
        max_diff = 1
    scale = 255.0 / max_diff
    ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)
    return ela_image

def prepare_image(image_path):
    return np.array(convert_to_ela_image(image_path, 90).resize(image_size)).flatten() / 255.0

def predict_image_type(image_path):
    processed_image = prepare_image(image_path)
    processed_image = processed_image.reshape(1, 128, 128, 3)
    prediction = model.predict(processed_image)
    pred_class = np.argmax(prediction, axis=1)[0]
    class_names = ['Real', 'Splicing', 'Copy-move']
    result = class_names[pred_class]
    confidence = prediction[0][pred_class] * 100
    return result, confidence


