import time
import RPi.GPIO as GPIO
import speaker

class Buzzer():
    def __init__(self):
        self.delay = 1
        self.pin = 18
        self.duty = 20
        self.freq = 900
        self.beep_time = 0.2
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.buzzer = GPIO.PWM(self.pin, self.freq)
    
    def beep(self, beep_time):
        self.start()
        speaker.play(beep_time)
        self.stop()
        time.sleep(beep_time)

    def start(self):
        self.buzzer.start(self.duty)

    def stop(self):
        self.buzzer.stop()