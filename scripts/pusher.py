#!/usr/bin/python
# pipx foo.hex=inp:[beh]

import sys
import serial
import time

buffer_size = 4096
wait_time = 8
sent = 0

s = serial.serial_for_url("spy:///dev/ttyUSB0", baudrate=1200, bytesize=serial.SEVENBITS, parity=serial.PARITY_ODD)

try:
    for line in sys.stdin:
        line = line.strip('\r\n') + '\r\n'
        line = line.encode('ascii', 'replace')
        sent += len(line)
        if sent > buffer_size:
            s.flush()
            time.sleep(1/30)
            s.write(b'\x13\r\n')
            time.sleep(1/30)
            s.flush()
            time.sleep(wait_time)
            sent = len(line)
        s.write(line)
        s.flush()
        time.sleep(1/30)
finally:
    s.write(b'\x13')
    time.sleep(wait_time)
    s.write(b'\x1a')
