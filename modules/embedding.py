# modules/embedding.py
# ArcFace face embedding using ONNX Runtime (Windows-safe)

import cv2
import numpy as np
import onnxruntime as ort
import os

# Path to ArcFace ONNX model
MODEL_PATH = os.path.join("models", "arcface_r50_v1.onnx")

# Load ArcFace ONNX model (CPU)
session = ort.InferenceSession(
    MODEL_PATH,
    providers=["CPUExecutionProvider"]
)

input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

def preprocess(face_img):
    """
    Preprocess face image for ArcFace
    """
    face_img = cv2.resize(face_img, (112, 112))
    face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
    face_img = face_img.astype(np.float32)
    face_img = (face_img - 127.5) / 128.0
    face_img = np.transpose(face_img, (2, 0, 1))
    face_img = np.expand_dims(face_img, axis=0)
    return face_img

def get_embedding(face_img):
    """
    face_img: numpy array (H, W, 3)
    returns: 512-dimensional ArcFace embedding
    """
    blob = preprocess(face_img)

    embedding = session.run(
        [output_name],
        {input_name: blob}
    )[0][0]

    # L2 normalization
    embedding = embedding / np.linalg.norm(embedding)
    return embedding
