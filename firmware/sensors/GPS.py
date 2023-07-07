import serial
import pynmea2
import time
import math

class GPS():
    def __init__(self):
        self.port = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=0.5)
        self.last_data = [0, 0]
        self.new_data = [0, 0]
        self.last_time = time.time()
        self.new_time = time.time()
        self.speed = 0
    
    def read(self):
        lines = self.port.read_all().decode('utf-8', errors='ignore')
        lines = lines.split('\n')
        while len(lines):
            line = lines.pop()
            if line[0:6] == '$GPRMC':
                data = pynmea2.parse(line)
                if data.latitude != 0 and data.longitude != 0:
                    self.last_data = self.new_data
                    self.last_time = self.new_time
                    self.new_data = [data.latitude, data.longitude]
                    self.new_time = time.time()
                    self.speed = self.calc_speed()
                    break
        return self.new_data

    def get_speed(self):
        return self.speed
    
    def calc_speed(self):
        lat1 = self.last_data[0]
        lon1 = self.last_data[1]
        lat2 = self.new_data[0]
        lon2 = self.new_data[1]
        if (lat1 == 0.0 and lon1 == 0.0) or (lat2 == 0.0 and lon2 == 0.0):
            return 0
        R = 6378.137
        dLat = lat2 * math.pi / 180 - lat1 * math.pi / 180
        dLon = lon2 * math.pi / 180 - lon1 * math.pi / 180
        a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(lat1 * math.pi / 180) * math.cos(lat2 * math.pi / 180) * math.sin(dLon/2) * math.sin(dLon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = R * c
        return d / ((self.new_time - self.last_time)/(60*60))