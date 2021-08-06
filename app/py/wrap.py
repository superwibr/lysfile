import lysdata as lys

##################
# CONSTANTS
_MNUM = 0x894C59530D0A1A0A or b'\211LYS\r\n\032\n'
_FTYPES = {
	0x0010 : "Typeless",
	0x0011 : "Bundle",
	0x0012 : "Links",
	0x0013 : "Interactive book",
	0x0014 : "Readable bundle",
	0x0015 : "AudioLoop",
}
_CTYPES = {
	0x0030 : "Typeless entry",
	0x0031 : "File",
	0x0032 : "JSON",
	0x0033 : "ReadableSection",
	0x0034 : "AudioSection",
	0x003f : "EOF",
}

###############
# CHUNK READER
def readChunk():
	pass

################
# MAIN FUNC
def read(path:str):
	reader 	= open(path, 'rb')
	data 	= reader.read()
	input	= lys.DataInput(data)

	lf={}

	lf['id'] = input.readU(8)
	if lf['id'] != _MNUM:
		raise Exception('[LYS Reader] Incorrect magic number! File may be:\n- Not in LYS format\n- Corrupt\n- Outdated')

	lf['ver'] = input.readU(2)
	if lf['ver'] <= 0x0001:
		raise Exception('[LYS Reader] Version is below 1! File may be corrupt.')

	lf['typ'] = input.readU(2)
	if lf['typ'] not in _FTYPES:
		raise Exception('[LYS Reader] LYSfile type not an accepted type! File may be corrupt or outdated.')

	return lf

