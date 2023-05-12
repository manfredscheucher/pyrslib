# author: Manfred Scheucher (2016-2023)

from RotationSystem import RotationSystem
from FileReader import FileReader
import struct

class RotationSystemBinaryReader(FileReader):
	def __init__(self,n,filepath,offset=0):
		super(RotationSystemBinaryReader,self).__init__(n,filepath,offset)		
		self.bytes = 1

	def _unpack(self,string):
		# http://docs.python.org/2/library/struct.html#format-characters
		if self.bytes == 1: return struct.unpack("<B",string)[0]
		if self.bytes == 2: return struct.unpack("<H",string)[0]
		if self.bytes == 4: return struct.unpack("<I",string)[0]
		if self.bytes == 8: return struct.unpack("<Q",string)[0]

		raise("ERROR: Invalid bytes!")

	def read_next(self):
		orientations = [range(1,self.n)]

		for i in range(1,self.n):
			orientations.append([])
			for j in range(self.n-1):
				b = self.f.read(self.bytes)
				if b == "": return None # end of file reached
				
				b = self._unpack(b)
				if j == 0:
					assert(b == self.index0) 
				orientations[i].append(b-self.index0)
			
		return RotationSystem(self.n,orientations)
