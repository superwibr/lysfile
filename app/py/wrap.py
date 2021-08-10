from  . import data as lys

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
	0x0016 : "BJTEMP"
}
def _FTYPESS(search):
	return (list(_FTYPES.keys())[list(_FTYPES.values()).index(search)])

_CTYPES = {
	0x0030 : "Typeless entry",
	0x0031 : "File",
	0x0032 : "JSON",
	0x0033 : "ReadableSection",
	0x0034 : "AudioSection",
	0x003f : "EOF",
}

###############
#  READER
class Reader:
	def __init__(self, path):
		with open(path, 'rb') as reader:
			self._data 	= reader.read()
			self._input	= lys.DataInput(self._data)

	def readChunk(self):
		chunk = 0
		return chunk

	def read(self):
		input = self._input
		lf={
			"id":"",
			"ver":0,
			"typ":"",
			"chunks":[]
		}

		lf['id'] = input.readU(8)
		if lf['id'] != _MNUM:
			raise Exception('[LYS Reader] Incorrect magic number! File may be not in LYS format, corrupt or outdated.')
		lf['id'] = _MNUM

		lf['ver'] = input.readU(2)
		if lf['ver'] < 0x0001:
			raise Exception('[LYS Reader] Version is below 1! File may be corrupt.')

		lf['typ'] = input.readU(2)
		if lf['typ'] not in [*_FTYPES]:
			raise Exception('[LYS Reader] LYSfile type not an accepted type! File may be corrupt or outdated.')

		lf['typ'] = _FTYPES[lf['typ']]
		if lf['typ'] == "BJTEMP":
			bj = self._data[12:]
			j = bj.decode("utf-8")

			lf['BJTEMP']=j
			return lf

		return lf

###############
#  WRITER
class Writer:
	def __init__(self, outFile, inFile=None):
		self._writer = open(outFile, 'wb')
		self._output	= lys.DataOutput()
		
		if inFile:
			with open(inFile, 'rb') as input:
				self._input = input.read()

		self._type = _FTYPESS("BJTEMP")# current default, change later

	def writeChunk(self):
		pass

	def write(self):
		o = self._output

		# Assembling header
		o.writeU(8, _MNUM)						;print("[LYS Writer] Pushed magic number to bytes")
		o.writeU(2, 0x0001)						;print("[LYS Writer] Pushed version to bytes")
		o.writeU(2, self._type)					;print("[LYS Writer] Pushed type to bytes")

		# Writing body
		if self._type == _FTYPESS("BJTEMP"):
			o.writeU(len(self._input), self._input)
			if len(self._input) % 2 != 0:
				o.writeU(1, 0x00)


		# write, close file and return
		self._writer.write(o.returnBytes())		;print("[LYS Writer] Wrote bytes to output file")
		self._writer.close()					;print("[LYS Writer] Closed output file")
		return

