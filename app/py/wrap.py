from inspect import EndOfBlock
from  . import data as lys
import bson
import json
from err import *

##################
# CONSTANTS
_MNUM = 0x894C59530D0A1A0A or b'\211LYS\r\n\032\n'
_FTYPES = {
	0x0010 : "NTYP",
	0x0011 : "BUNDL",
	0x0012 : "LINKS",
	0x0014 : "RBUND",
	0x0016 : "BJTEMP"
}
def _FTYPESS(search):
	return (list(_FTYPES.keys())[list(_FTYPES.values()).index(search)])

_CTYPES = {
	0x0030 : "Typeless entry",
	0x0031 : "File",
	0x0032 : "JSON",
	0x0033 : "ReadableSection",
	0x003f : "EOF",
}
def _CTYPESS(search):
	return (list(_CTYPES.keys())[list(_CTYPES.values()).index(search)])

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
			raise IllegalIdentifierError('[LYS Reader] Incorrect magic number! File may be not in LYS format, corrupt or outdated.')
		lf['id'] = _MNUM

		lf['ver'] = input.readU(2)
		if lf['ver'] < 0x0001:
			raise IllegalIdentifierError('[LYS Reader] Version is below 1! File may be corrupt.')

		lf['typ'] = input.readU(2)
		if lf['typ'] not in [*_FTYPES]:
			raise IllegalIdentifierError('[LYS Reader] LYSfile type not an accepted type! File may be corrupt or outdated.')

		lf['typ'] = _FTYPES[lf['typ']]
		if lf['typ'] == "BJTEMP":
			bj = self._data[12:]
			j = bson.loads(bj)
			lf["chunks"].append(j)
			return lf

		return lf

###############
#  WRITER
class Writer:
	def __init__(self, outFile, inFile):
		self._outPath 	= outFile
		self._output	= lys.DataOutput()
		self._inPath	= inFile
		
		with open(inFile, 'rb') as input:
			self._input = input.read()
			self._input = json.loads(self._input)

		self._type = _FTYPESS(self._input['type'])

	def writeChunk(self, chunk):
		o = self._output

		o.writeU(2, _CTYPESS(chunk['type']))
		content=None

		if chunk['type'] == None:
			raise MissingChunkTypeError("[LYS Writer] A chunk type could not be found!")
		elif chunk['type'] == 'Typeless':
			pass
		elif chunk['type'] == 'File':
			with open(chunk['src'], 'rb') as fileread:
				content = fileread.read()
		elif chunk['type'] == 'JSON':
			pass
		elif chunk['type'] == 'ReadableSection':
			pass
		elif chunk['type'] == 'EOF':
			return 'EOF'
		else:
			raise IllegalChunkTypeError(f"[LYS Writer] Chunk type \"[{chunk['type']}\" invalid!")

		o.writeU(6, len(content))

		return

	def writeChunks(self, accepted):
		chunks = self._input['chunks']
		for chunk in chunks:
			if chunk['type'] not in accepted:
				raise IllegalChunkTypeError(f"[LYS Writer] Chunk of type {chunk['type']} not accepted for LYS document of type {self._input['type']}")
			else:
				ret = self.writeChunk(chunk)
				if ret == 'EOF': break
		return

	def write(self):
		o = self._output

		# Assembling header
		o.writeU(8, _MNUM)						;print("[LYS Writer] Pushed magic number to bytes")
		o.writeU(2, 0x0001)						;print("[LYS Writer] Pushed version to bytes")
		o.writeU(2, self._type)					;print("[LYS Writer] Pushed type to bytes")

		# Writing body
		if self._input['type'] == _FTYPESS("BJTEMP"):
			content = self._input['chunks'][0]['content']
			lbson = bson.dumps(content) 
			o.writeU(len(lbson), lbson)
			if len(content) % 2 != 0:
				o.writeU(1, 0x00)

		elif self._type == _FTYPESS("BUNDL"):
			self.writeChunks(["File"])


		# write, close file and return
		writer = open(self._outPath, 'wb')	;print("[LYS Writer] Opened output file")
		writer.write(o.returnBytes())		;print("[LYS Writer] Wrote bytes to output file")
		writer.close()						;print("[LYS Writer] Closed output file")
		return

