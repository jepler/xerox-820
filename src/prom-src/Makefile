.PHONY: default
default:
	rm -f XRXPL.LST XRXPL.REL XRXPH.LST XRXPH.REL XPRP.HEX
	iz-cpm m80.com =XRXPL.MAC/L
	iz-cpm m80.com =XRXPH.MAC/L
	((echo '/P:0,XRXPL,XRXPH,XRXP/N/X/E'; echo Y) | timeout 5 iz-cpm l80.com)  || true
	./z80eof.py XRXP.HEX
