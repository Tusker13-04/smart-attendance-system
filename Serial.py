import serial
arduino=serial.Serial(port="COM3",baudrate=9600)
while True:
    print(str(arduino.readline()))