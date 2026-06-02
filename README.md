# Image Forgery Detection System

## Overview

The Image Forgery Detection System is a deep learning-based application designed to identify manipulated digital images. The system detects and classifies images into three categories:

- Real Image
- Copy-Move Forgery
- Splicing Forgery

The project combines Error Level Analysis (ELA), Convolutional Neural Networks (CNN), and EXIF Metadata Analysis to improve the reliability of forgery detection.

---

## Features

- Detects image tampering automatically
- Classifies images as Real, Copy-Move, or Splicing
- Uses Error Level Analysis (ELA) for feature extraction
- Performs EXIF metadata inspection
- User-friendly Flask web interface
- Real-time image upload and prediction
- Deep learning-based classification using TensorFlow/Keras

---

## Technologies Used

### Programming Language
- Python

### Machine Learning & Deep Learning
- TensorFlow
- Keras
- CNN (Convolutional Neural Network)

### Image Processing
- OpenCV
- Pillow (PIL)
- Error Level Analysis (ELA)

### Web Framework
- Flask

### Frontend
- HTML
- CSS
- JavaScript

### Metadata Analysis
- EXIF Metadata Processing

---

## Project Structure

```
image_forgery_detection_system/
│
├── project code/
│   ├── app.py
│   ├── predict.py
│   ├── metadata.py
│   ├── best_forgery_classifier1.h5
│   └── templates/
│       ├── index.html
│       └── result.html
│
├── model_training_code.ipynb
├── .gitignore
├── .gitattributes
└── README.md
```

---

## Methodology

### 1. Image Upload
The user uploads an image through the Flask web interface.

### 2. Error Level Analysis (ELA)
The uploaded image undergoes ELA preprocessing to highlight compression differences and possible tampered regions.

### 3. CNN-Based Classification
The processed image is passed through a trained Convolutional Neural Network that predicts whether the image is:

- Real
- Copy-Move Forgery
- Splicing Forgery

### 4. Metadata Analysis
The system analyzes available EXIF metadata and provides additional information regarding image authenticity.

### 5. Result Generation
The final prediction is displayed through the web interface.

---

## Dataset

The model was trained using the casia dataset containing:
Authentic images (Au)
- Real Images
Tampered images (Tp)
- Copy-Move Forged Images
- Splicing Forged Images

The dataset was preprocessed using Error Level Analysis before training.

---

## Applications

- Digital Forensics
- Journalism and Media Verification
- Cybersecurity Investigations
- Legal Evidence Validation
- Social Media Content Verification

---

## Future Enhancements

- Localization of forged regions
- Support for additional forgery types
- Transformer-based deep learning models
- Cloud deployment
- Mobile application integration

---

## Disclaimer

This repository may contain code, libraries, or resources developed by third parties. All rights belong to their respective owners. This repository is intended for educational and research purposes only. Some portions of the code may have been developed with assistance of AI tools.

---
