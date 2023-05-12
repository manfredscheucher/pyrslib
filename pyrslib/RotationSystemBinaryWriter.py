# author: Manfred Scheucher (2016-2023)

from FileWriter import FileWriter
import struct

from RotationSystem import RotationSystem

class RotationSystemBinaryWriter(FileWriter):
	def __init__(self,n,filepath,always_flush=False,lazy_open=True,offset=0):
		super(RotationSystemBinaryWriter,self).__init__(n,filepath,always_flush,lazy_open,offset)
		self.bytes = 1

	def _pack(self,value):
		# http://docs.python.org/2/library/struct.html#format-characters
		if self.bytes == 1: return struct.pack("<B",value)
		if self.bytes == 2: return struct.pack("<H",value)
		if self.bytes == 4: return struct.pack("<I",value)
		if self.bytes == 8: return struct.pack("<Q",value)
		raise("ERROR: Invalid bytes!")

	def _write_next(self,rs):
		try:
			s = ""
			for i in range(1,rs.n):
				for j in range(rs.n-1):
					b = rs.orientations[i][j]+self.index0
					s += self._pack(b)

			self.f.write(s)

		except struct.error:
			print "DATA ERROR @ RS",rs
