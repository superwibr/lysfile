class DataInput:
	def __init__(self, stream):
		self._stream   = stream
		self._length   = len(stream)
		self._position = 0

	# Reading unsigned integers
	def readU8(self):
		if self._position >= self._length:
			Exception("[LYS data] reader position ran off the end of the file!")
		value = self._stream[self._position]
		self._position+=1
		return value

	def readU(self, bytes:int): 
		value = 0
		multiple = bytes*8-8
		while multiple >= 0:
			value |= self.readU8() << multiple
			multiple -= 8
		return value

	# Reading signed integers
	def readS8(self):
		value = self.readU8()
		if value >> 7 == 1 :
			value = ~( value ^ 0xFF )
		return value

	def readS(self, bytes:int):
		value = self.readU(bytes)
		if value >> (bytes*8-1) == 1 :
			value = ~( value ^ 0xFF )
		return value


class DataOutput:
	def __init__(self):
		self._stream = []
		self._position = 0

	# Write unsigned integers
	def writeU8(self, value:int):
		value &= 0xFF
		self._stream.append(value)
		self._position+=1

	def writeU(self, nbytes:int, value:int):
		nbc = nbytes
		andmt = ""
		while nbc > 0:
			andmt+="ff"
			nbc-=1

		if type(value) == bytes:
			value = int.from_bytes(value, byteorder='big')
			
		value = value & int(andmt, base=16)

		multiple = nbytes*8-8
		while multiple >= 0:
			if multiple < 0:
				break
			self.writeU8( value >> multiple)
			multiple-=8
		return value

	# return 
	def returnBytes(self):
		return bytes(self._stream)
