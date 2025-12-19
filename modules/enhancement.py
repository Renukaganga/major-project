# modules/enhancement.py
# Image Enhancement using EDSR + CLAHE (Windows-safe)

import cv2
import numpy as np
import os

# Absolute path to model file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "EDSR_x2.pb")

# Initialize Super Resolution model
sr = cv2.dnn_superres.DnnSuperResImpl_create()
sr.readModel(MODEL_PATH)
sr.setModel("edsr", 2)

def enhance_image(image_input):
    """
    image_input:
      - Streamlit UploadedFile
      - OR numpy array (BGR image)
    """

    if hasattr(image_input, "read"):
        img_array = np.frombuffer(image_input.read(), np.uint8)
        image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    else:
        image = image_input

    # Super-resolution
    sr_image = sr.upsample(image)

    # CLAHE for contrast enhancement
    lab = cv2.cvtColor(sr_image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)

    enhanced = cv2.merge((cl, a, b))
    enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)

    return enhanced
