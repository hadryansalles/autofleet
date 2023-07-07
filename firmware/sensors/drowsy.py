import cv2
import dlib
import time
from imutils import face_utils as face
from scipy.spatial import distance
import imutils

EYE_DROWSINESS_THRESHOLD    = 0.17
EYE_DROWSINESS_INTERVAL     = 1.2
NULL_INTERVAL = 5

drowsy_states = ['Error', 'Undetected', 'Normal', 'Drowsy']

def get_max_area_rect(rects):
    if len(rects) == 0:
        return None
    areas=[]
    for rect in rects:
        areas.append(rect.area())
    return rects[areas.index(max(areas))]

def get_eye_aspect_ratio(eye):
    vertical_1 = distance.euclidean(eye[1], eye[5])
    vertical_2 = distance.euclidean(eye[2], eye[4])
    horizontal = distance.euclidean(eye[0], eye[3])
    return (vertical_1+vertical_2)/(horizontal*2)

class Drowsy():
    def __init__(self, camId, debug):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor('/home/autofleet/autofleet/sensors/shape_predictor_68_face_landmarks.dat')
        self.ls, self.le = face.FACIAL_LANDMARKS_IDXS["left_eye"]
        self.rs, self.re = face.FACIAL_LANDMARKS_IDXS["right_eye"]

        self.cap = cv2.VideoCapture(camId)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.cap.set(cv2.CAP_PROP_FPS, 3)
        self.state = 0
        self.last_open_eye = -1
        self.debug = debug

    def get_state(self):
        _ , frame = self.cap.read()
        frame = cv2.flip(frame, 1)
        frame = cv2.flip(frame, 0)
        self.process_frame(frame)
        if self.debug:
            key = cv2.waitKey(5)&0xFF
            cv2.imshow("Drowsy", frame)
        print(f'{drowsy_states[self.state + 1]} DRIVER.')
        return self.state

    def process_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = self.detector(gray, 0)
        rect = get_max_area_rect(rects)

        if rect != None:
            shape = self.predictor(gray, rect)
            shape = face.shape_to_np(shape)
            leftEye = shape[self.ls:self.le]
            rightEye = shape[self.rs:self.re]
            leftEAR = get_eye_aspect_ratio(leftEye)
            rightEAR = get_eye_aspect_ratio(rightEye)
            ear = (leftEAR + rightEAR) / 2.0
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(frame, [leftEyeHull], -1, (255, 255, 255), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (255, 255, 255), 1)

            if ear < EYE_DROWSINESS_THRESHOLD:
                if time.time() - self.last_open_eye >= EYE_DROWSINESS_INTERVAL:
                    self.state = 2
            else:
                self.last_open_eye = time.time()
                self.state = 1
        elif time.time() - self.last_open_eye >= NULL_INTERVAL:
            self.state = 0
