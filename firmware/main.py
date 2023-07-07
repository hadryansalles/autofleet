import time
import threading
import streamer
import buzzer

IN_RASPBERRY = True
USE_STREAMER = True
HANDS_DEBUG = False
DROWSY_DEBUG = False

# SCENE_ID = 7

DEVICE_ID = 7
url = ':)'

DROWSY_CAMERA_DEVICE = 0
HANDS_CAMERA_DEVICE = 2

BUZZER_DELAY_ERROR = 0.8
BUZZER_DELAY_WARNING = 0.2

if IN_RASPBERRY:
    from sensors import accelerometer, GPS, drowsy, hands
else:
    from fake_sensors import accelerometer, GPS
    from sensors import drowsy, hands

# update times in seconds
acc_ut = 4
gps_ut = 2
streamer_ut = 6
drowsy_ut = 0
hands_ut = 1

acc_data = [[0.0, 0.0, 0.0]]
gps_data = [0.0, 0.0]
speed_data = [0.0]
drowsy_data = -1
hands_data = -2

buzzer_delay = BUZZER_DELAY_ERROR

def get_max_acc():
    global acc_data
    print(acc_data)
    max_acc = max(acc_data, key=lambda acc: acc[0]**2 + acc[1]**2 + acc[2]**2)
    acc_data = []
    return max_acc

def get_max_speed():
    global speed_data
    if(len(speed_data) == 0):
        return 0
    max_speed = max(speed_data)
    speed_data = []
    return max_speed

def update_buzzer():
    global drowsy_data
    global hands_data
    global buzzer_delay
    buzzer_delay = -1
    return

    if hands_data <= -1 or drowsy_data <= 0:
        buzzer_delay = BUZZER_DELAY_ERROR
    elif hands_data < 2 or drowsy_data == 2:
        buzzer_delay = BUZZER_DELAY_WARNING
    else:
        buzzer_delay = -1

def drowsy_run():
    global drowsy_data
    while True:
        try:
            d = drowsy.Drowsy(DROWSY_CAMERA_DEVICE, DROWSY_DEBUG)
            while True:
                drowsy_data = d.get_state()
                time.sleep(drowsy_ut)
        except Exception as e:
            print('Exception in drowsy thread: ', str(e))

def hands_run():
    global hands_data
    while True:
        try:
            h = hands.Hands(HANDS_CAMERA_DEVICE, HANDS_DEBUG)
            last_time = 0
            while True:
                h.capture()
                if time.time() - last_time > hands_ut:
                    hands_data = h.get_hands()
                    last_time = time.time()
        except Exception as e:
            print('Exception in hands thread: ', str(e))

def gps_run():
    global gps_data
    global speed_data
    while True:
        try:
            gps = GPS.GPS()
            while True:
                gps_data = gps.read()
                speed_data.append(gps.get_speed())
                time.sleep(gps_ut)
        except Exception as e:
            print('Exception in gps thread: ', str(e))

def acc_run():
    global acc_data
    while True:
        try:
            accelerometer.init()
            while True:
                acc_data.append(accelerometer.read())
                time.sleep(acc_ut)
        except Exception as e:
            print('Exception in accelerometer thread: ', str(e))

def streamer_run():
    while True:
        try:
            s = streamer.Streamer(url, DEVICE_ID)
            time.sleep(streamer_ut)
            while True:
                s.send_history(speed=get_max_speed(), acc=get_max_acc(), gps=gps_data, drowsy=drowsy_data, hands=hands_data)
                time.sleep(streamer_ut)
        except Exception as e:
            print('Exception in streamer thread: ', str(e))

def buzzer_run():
    global buzzer_delay
    while True:
        try:
            b = buzzer.Buzzer()
            while True:
                if buzzer_delay != -1:
                    b.beep(buzzer_delay)
                else:
                    time.sleep(0.1)
                update_buzzer()
        except Exception as e:
            print('Exception in buzzer thread: ', str(e))

def main():
    print('Starting threads...')
    buzzer_thread = threading.Thread(target=buzzer_run)
    buzzer_thread.start()

    acc_thread = threading.Thread(target=acc_run)
    acc_thread.start()

    gps_thread = threading.Thread(target=gps_run)
    gps_thread.start()

    drowsy_thread = threading.Thread(target=drowsy_run)
    drowsy_thread.start()

    hands_thread = threading.Thread(target=hands_run)
    hands_thread.start()

    streamer_thread = threading.Thread(target=streamer_run)
    streamer_thread.start()

    buzzer_thread.join()
    acc_thread.join()
    gps_thread.join()
    drowsy_thread.join()
    hands_thread.join()
    streamer_thread.join()

if __name__ == '__main__':
    main()
