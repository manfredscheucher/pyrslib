# author: Manfred Scheucher (2016-2023)

from abc import ABCMeta, abstractmethod

class FileWriter(object):
	__metaclass__ = ABCMeta

	def __init__(self,n,filepath,always_flush,lazy_open,offset):
		self.n = n
		self.filepath = filepath
		self.always_flush = always_flush
		if not lazy_open: 
			self._open_file()
		self.index0 = offset
		assert(self.index0 in [0,1])

	def _open_file(self): 
		self.f = open(self.filepath,"w")

	def write(self,rs,flush=False):
		try:
			testf = self.f
		except AttributeError:
			self._open_file()

		self._write_next(rs)

		if flush or self.always_flush: 
			self.f.flush()

	@abstractmethod
	def _write_next(self,rs): pass
