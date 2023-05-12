import os
import serial

s = serial.Serial("/dev/ttyUSB0", baudrate=1200, bytesize=serial.SEVENBITS, parity=serial.PARITY_ODD)

s.write(b'\n')
while True:
    print(s.readline().decode('ascii', 'replace').replace('\r\n', ''))
    s.write(b'\n')

