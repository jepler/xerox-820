.PHONY: default
default: XMODEM5.hex XMODEM5.com

%.hex: %.ASM
	../host-src/zasm/zasm --asm8080 $<  -x --target=ram -uw

%.com: %.ASM
	../host-src/zasm/zasm --asm8080 $<  -uw $@
