Bytes (big-endian)
	+00 8B Magic number (0x894c59530d0a1a0a)
	+08 2B Version number (presently 1)
	+09 2B LYSfile type
	+0a *B *Chunks
		+00 2B Chunk type ID 
		+04 6B Chunk length (in bytes)
		+08 *B Chunk data
	+0a 4B EOF

LYSfile types
	0x0010 Typeless
	0x0011 Bundle
	0x0012 Links
	0x0014 Readable bundle
	0x0016 BJTEMP

Chunk types
	0x0030 Typeless entry
	0x0031 File
	0x0032 JSON
	0x0033 ReadableSection
	0x003f EOF
