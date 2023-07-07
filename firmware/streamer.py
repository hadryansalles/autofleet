import requests
import time
import datetime
import pickle
import os

def datetime_str():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class Streamer():
    def __init__(self, url, device_id):
        self.url = url
        self.device_id = device_id
        self.trip_id = self.get_trip_id()
        self.batch_size = 100

    def buffer_file_name(self, api):
        return f'trip_{str(self.trip_id)}_{api[0:-1]}.bin'
    
    def load_buffer(self, api):
        buffer_file = self.buffer_file_name(api)
        buffer = []
        try:
            with open(buffer_file, 'rb') as f:
                buffer = pickle.load(f)
        except:
            pass
        return buffer
    
    def get_trip_id(self):
        r = requests.get(self.url + 'trip-device/' + str(self.device_id) + '/', timeout=5.0)
        r.raise_for_status()
        return r.json()['results'][0]['id']

    def dump_buffer(self, buffer, api, log=False):
        buffer_file = self.buffer_file_name(api)
        with open(buffer_file, 'w+b') as f:
            pickle.dump(buffer, f)
        if log:
            print(f"Dump buffer '{buffer_file}': {buffer}")

    def send(self, api, data):
        buffer = self.load_buffer(api)
        print(f'Processing new packet {data}')
        buffer.append(data)
        self.dump_buffer(buffer, api)
        try:
            last_index = min(len(buffer), self.batch_size)
            batch = buffer[0:last_index]
            r = requests.post(self.url + api, json=batch, timeout=5.0)
            if 200 <= r.status_code < 300:
                buffer = buffer[last_index + 1: len(buffer)]
                print(f'Success sending buffer with {last_index} packet(s)')
            else:
                raise f'Failed to send buffer: {r.status_code}'
        except:
            pass
        self.dump_buffer(buffer, api, log=False)
        print(f'Dumping {len(buffer)} packet(s) locally to {self.buffer_file_name(api)}')
        print('--------------------------------------------')

    def send_history(self, speed, gps, acc, drowsy, hands):
        packet = {
            'trip': self.trip_id,
            'acc_x': acc[0],
            'acc_y': acc[1],
            'acc_z': acc[2],
            'latitude': gps[0],
            'longitude': gps[1],
            'speed': speed,
            'date': datetime_str(),
            'drowsy_state': drowsy,
            'hands_state': hands
        }
        self.send('trip-history-batch/', packet)

    def send_drowsy_alert(self, duration, ratio):
        packet = {
            'trip': self.trip_id,
            'drowsy_ratio': ratio,
            'duration': duration,
            'date': datetime_str()
        }
        self.send('drowsy/', packet)

    def send_hands_off_alert(self, duration, n_hands):
        packet = {
            'trip': self.trip_id,
            'hands': n_hands,
            'duration': duration,
            'date': datetime_str()
        }
        self.send('handsoff/', packet)

if __name__ == '__main__':
    s = Streamer(':)', 1)
    s.send_history(12, (0, 10), (0, -12, 18))