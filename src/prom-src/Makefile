.PHONY: default
defaut: xrxp_f000.hex xrxp.com

xrxp.hex: xrxp.mac xrxpdef.mac
	../../bin/zmac --oo hex,lst $<
	cp zout/$@ $@

xrxp_com.hex: xrxp.mac xrxpdef.mac
	../../bin/zmac --oo hex,lst --od zcom -DAS_COM $<
	cp zcom/xrxp.hex $@

xrxp.com: xrxp_com.hex
	objcopy -I ihex -O binary $< $@

xrxp.bin: xrxp.hex
	objcopy -I ihex -O binary $< $@

xrxp_f000.bin: xrxp.bin
	dd bs=16 skip=1 if=$< of=$@

xrxp_f000.hex: xrxp_f000.bin
	objcopy --change-address=0xf000 -I binary -O ihex $< $@

xrxp_f000.inc: xrxp_f000.bin bin2h.py
	./bin2inc.py $< $@

testprom.com: testprom.mac xrxp_f000.inc
	
