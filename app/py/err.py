class Error(Exception):
	pass

class IllegalChunkTypeError(Error):
	def __init__(self, message):            
		super().__init__(message)

class IllegalIdentifierError(Error):
	def __init__(self, message):            
		super().__init__(message)