# Base
class Error(Exception):pass

# Illegal
class IllegalChunkTypeError(Error):pass
class IllegalFileTypeError(Error):pass
class IllegalIdentifierError(Error):pass

# Missing
class MissingChunkTypeError(Error):pass
class MissingFileTypeError(Error):pass
class MissingTypeError(Error):pass
class MissingValueError(Error):pass