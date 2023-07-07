import cv2
import mediapipe as mp
import time
mp_hands = mp.solutions.hands

HANDS_OFF_0_INTERVAL = 2
HANDS_OFF_1_INTERVAL = 5

class Hands:
    def __init__(self, camId, debug):
        self.cap = cv2.VideoCapture(camId)
        self.hands = mp_hands.Hands(model_complexity=0, min_detection_confidence=0.4, min_tracking_confidence=0.4)
        self.debug = debug
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.cap.set(cv2.CAP_PROP_FPS, 1)
        self.last_hands = 0
        self.last_init = -1
        self.frame = None
    
    def capture(self):
        success, self.frame = self.cap.read()
        if not success:
            raise Exception('Problem capturing from video device.')

    def get_hands(self):
        image = self.frame
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image)
        if self.debug:
            key = cv2.waitKey(5)&0xFF
            cv2.imshow("Hands", image)
        n_hands = 0
        if results.multi_handedness is not None:
            n_hands = len(results.multi_handedness)
        print(f'[{n_hands} STEERING WHEEL]')

        if n_hands > self.last_hands or n_hands == 2:
            self.last_init = time.time()

        self.last_hands = n_hands
        
        if n_hands == 1 and time.time() - self.last_init > HANDS_OFF_1_INTERVAL:
            return 1
        elif n_hands == 0 and time.time() - self.last_init > HANDS_OFF_0_INTERVAL:
            return 0
        else:
            return 2