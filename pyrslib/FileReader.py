# author: Manfred Scheucher (2016-2023)

from abc import ABCMeta, abstractmethod

class FileReader(object):
	__metaclass__ = ABCMeta

	def __init__(self,n,filepath,offset):
		self.n = n
		self.filepath = filepath
		self.f = open(filepath)
		self.index0 = offset
		assert(self.index0 in [0,1])

	def read_all(self):
		while True:
			rs = self.read_next()
			if rs == None: break 
			if not rs.is_valid(): print "FileReader invalid:",rs.to_string()
			assert(rs.is_valid())
			yield rs

	@abstractmethod
	def read_next(self,rs): pass
