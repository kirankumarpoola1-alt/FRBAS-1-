import cv2
import dlib
import numpy as np
from scipy.spatial import distance

detector = dlib.get_frontal_face_detector()
import os

PREDICTOR_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "shape_predictor_68_face_landmarks.dat"
)

predictor = dlib.shape_predictor(PREDICTOR_PATH)


LEFT_EYE = (42, 48)
RIGHT_EYE = (36, 42)
EAR_THRESHOLD = 0.25

def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

def detect_blink(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        shape = predictor(gray, face)
        shape = np.array([[p.x, p.y] for p in shape.parts()])

        left = shape[LEFT_EYE[0]:LEFT_EYE[1]]
        right = shape[RIGHT_EYE[0]:RIGHT_EYE[1]]

        ear = (eye_aspect_ratio(left) + eye_aspect_ratio(right)) / 2
        if ear < EAR_THRESHOLD:
            return True

    return False
