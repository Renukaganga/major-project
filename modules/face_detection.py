# modules/face_detection.py

import cv2
from mtcnn import MTCNN

detector = MTCNN()

def extract_face(image):
    """
    image: numpy array (H, W, 3)
    returns: cropped face image
    """
    results = detector.detect_faces(image)

    if len(results) == 0:
        return None

    x, y, w, h = results[0]["box"]
    x, y = max(0, x), max(0, y)
    face = image[y:y+h, x:x+w]

    return cv2.resize(face, (112, 112))
