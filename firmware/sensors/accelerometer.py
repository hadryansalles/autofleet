import smbus

# MPU6050 registers and their address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47

bus = smbus.SMBus(1)  # or bus = smbus.SMBus(0) for older version boards
device_address = 0x68 # MPU6050 device address

def init():
    # write to sample rate register
    bus.write_byte_data(device_address, SMPLRT_DIV, 7)
    # write to power management register
    bus.write_byte_data(device_address, PWR_MGMT_1, 1)
    # write to Configuration register
    bus.write_byte_data(device_address, CONFIG, 0)
    # write to Gyro configuration register
    bus.write_byte_data(device_address, GYRO_CONFIG, 24)
    # write to interrupt enable register
    bus.write_byte_data(device_address, INT_ENABLE, 1)

def read_raw_data(addr):
    # accelerometer and gyro value are 16-bit
    high = bus.read_byte_data(device_address, addr)
    low = bus.read_byte_data(device_address, addr+1)
    # concatenate higher and lower value to get signed value
    value = ((high << 8) | low)
    if(value > 32768):
        value = value - 65536
    return value

def read():
    acc_x = read_raw_data(ACCEL_XOUT_H)
    acc_y = read_raw_data(ACCEL_YOUT_H)
    acc_z = read_raw_data(ACCEL_ZOUT_H)
    return [acc_x, acc_y, acc_z]

def read_giroscope():
    gyro_x = read_raw_data(GYRO_XOUT_H)
    gyro_y = read_raw_data(GYRO_YOUT_H)
    gyro_z = read_raw_data(GYRO_ZOUT_H)
    return [gyro_x, gyro_y, gyro_z]