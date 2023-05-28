#!/usr/bin/python3
import binascii 
import serial
import struct
import sys
import time
import collections
import subprocess

counts = collections.Counter()

image_filename = sys.argv[1] if len(sys.argv) > 1  else "disk.img"
#port_url = sys.argv[2] if len(sys.argv) > 2 else "spy:////dev/ttyUSB0"
port_url = sys.argv[2] if len(sys.argv) > 2 else "/dev/ttyUSB0"
port = serial.serial_for_url(port_url, 307200)

def readhex(n):
    return binascii.a2b_hex(port.read(2*n))

NUM_TRACKS = 77
NUM_SECTORS = 26
content = bytearray(b'\xe5') * (128 * NUM_TRACKS * NUM_SECTORS)

last_track = -1
error_count = 0
t00 = t0 = time.monotonic()
while True:
    c = port.read(1)
    if c != b':': continue

    header = readhex(4)
    data_len, address, rectype = struct.unpack('>BHB', header)
    #print(f"record {data_len=} {address=:04x} {rectype=:02d} ")
    if rectype & 0xf0 == 0xf0:
        data = port.read(data_len)
    else:
        data = readhex(data_len)
    checksum = readhex(1)
    #print(f"{data=} {checksum=}")

    if sum(header + data + checksum) % 256 != 0:
        count['CHECKSUM_ERROR'] += 1
        print("# Checksum error!")

    c = port.read(1)
    if c not in (b'\r', b'\n'):
        count['FRAMING_ERROR'] += 1
        print(f"# Expected newline missing! {c=}")

    if rectype in (0x80, 0x81, 0xe5):
        track = data[0]
        sector = data[1]
        status = ("OK" if rectype == 0x80 else
                "EMPTY" if rectype == 0xe5 else "READ_ERROR")
        counts[status] += 1
        linear_address = (NUM_SECTORS * track + sector - 1) * 128
        sector_data = memoryview(content)[linear_address:linear_address+128]
        if track != last_track:
            t1 = time.monotonic()
            if last_track > 0:
                print(end=f" track time {t1-t0:.1f}s")
            t0 = t1
            print(end=f"\n{track:2d} ", flush=True)
            last_track = track
        print(chr(64 + sector) if status == "OK" else "_" if status == "EMPTY" else "!", end="", flush=True)
        #print(f"T{track:02} S{sector:02d} {status}")
    elif rectype in (0x0, 0xf1):
        sector_data[address:address+data_len] = data
        counts["DATA"] += 1
    elif rectype == 0x1: # EOD
        break
    else:
        count[f'UNKNOWN_{rectype:02x}'] += 1
t1 = time.monotonic()

print()
print(counts)

with open(image_filename, "wb") as f:
    f.write(content)

subprocess.run(["cpmls", "-F", image_filename])
print(f"imaged in {t1-t00:.1f}s")
