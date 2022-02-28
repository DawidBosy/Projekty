import sys
import serial
import time

class ArduinoInputReader:
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        self.ser.reset_input_buffer()

    def get_input(self):
        data = self.ser.readline().decode('ascii').rstrip()
        self.ser.reset_input_buffer()
        
        try:
            x, y, z, b1, b2 = [int(i) for i in data.split(',')]
        except:
            x, y, z, b1, b2 = 512, 512, 1, 1, 1
            
        return x, y, z, b1, b2