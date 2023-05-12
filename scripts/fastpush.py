# pipx foo.hex=inp:[beh]

import sys
import serial
import time

baudrate = 9600
if len(sys.argv) > 1: baudrate = int(sys.argv[1])
buffer_size = 4096
wait_time = 8
sent = 0

s = serial.serial_for_url("spy:///dev/ttyUSB0", baudrate=baudrate, bytesize=serial.SEVENBITS, parity=serial.PARITY_ODD)

try:
    for line in sys.stdin:
        line = line.strip('\r\n') + '\r\n'
        line = line.encode('ascii', 'replace')
        sent += len(line)
        if sent > buffer_size:
            s.flush()
            s.write(b'\x13\r\n')
            s.flush()
            time.sleep(wait_time)
            sent = len(line)
        s.write(line)
finally:
    s.write(b'\x13')
    s.write(b'\x1a')
