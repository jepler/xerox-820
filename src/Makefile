.PHONY: default
default: XMODEM5.hex

%.hex: %.ASM
	./host-src/zasm/zasm --asm8080 $<  -x --target=ram -uw
