#!/usr/bin/python
import sys

z80_eof = 26

with open(sys.argv[1], 'rb') as f:
    content = f.read()

if (idx := content.find(z80_eof)) != -1:
    content = content[:idx]
    with open(sys.argv[1], 'wb') as f:
        f.write(content)
