.PHONY: default
defaut: xrxp_f000.hex

xrxp.hex: xrxp.mac xrxpdef.mac
	../../bin/zmac --oo hex,lst $<
	cp zout/$@ $@

xrxp.bin: xrxp.hex
	objcopy -I ihex -O binary $< $@

xrxp_f000.bin: xrxp.bin
	dd bs=16 skip=1 if=$< of=$@

xrxp_f000.hex: xrxp_f000.bin
	objcopy --change-address=0xf000 -I binary -O ihex $< $@
