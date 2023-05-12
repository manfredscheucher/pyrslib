# author: Manfred Scheucher (2016-2023)

import sys
from datetime import datetime
from abc import ABCMeta, abstractmethod
from ArgumentReader import ArgumentReader
from RotationSystemTextReader import RotationSystemTextReader
from RotationSystemBinaryReader import RotationSystemBinaryReader
from RotationSystemTextWriter import RotationSystemTextWriter
from RotationSystemBinaryWriter import RotationSystemBinaryWriter

class BasicScript(object): 
	def __init__(self,automatic_output_writer=True):
		if len(sys.argv) == 1:
			self._print_usage_info(sys.argv)
			print "default parameters:"
			print "\tn - number of points"
			print "\tft - filetype (rsb0 / rst0 / rsb1 / rst1)"
			print "\tfp - filepath"
			exit(-1)

		self.automatic_output_writer = automatic_output_writer
		self.arguments = ArgumentReader(sys.argv)
		self.DEBUG = int(self.arguments.get("DEBUG",0))

		self.outfile_suffix = ""
		self.reader = None
		self.writer = None

		self.n = int(self.arguments.get("n"))
		self.filepath = self.arguments.get("fp")
		ending = self.filepath.split('.')[-1]
		
		self.filetype = self.arguments.get("ft",ending)

		if self.filetype == "b08":
			self.filetype = "rsb1"

		if self.filetype == "txt":
			self.filetype == "rst1"

		self.outfilepath = self.arguments.get("ofp",self.filepath)
		self.outfiletype = self.arguments.get("oft",self.filetype)

		self.from_ = int(self.arguments.get("from",0))
		self.to_ = int(self.arguments.get("to",0))

		if self.from_ or self.to_:
			self.outfilepath += ".from_"+str(self.from_)+"_to_"+str(self.to_)

	@abstractmethod
	def _print_usage_info(self,argv): pass

	@abstractmethod
	def _action_inner(self,rs): pass

	@abstractmethod
	def _action_end(self): pass

	def _init_files(self):
		if self.filetype == "rsb0":
			self.reader = RotationSystemBinaryReader(self.n,self.filepath,offset=0)
		elif self.filetype == "rsb1":
			self.reader = RotationSystemBinaryReader(self.n,self.filepath,offset=1)
		elif self.filetype == "rst0":
			self.reader = RotationSystemTextReader(self.n,self.filepath,offset=0)
		elif self.filetype == "rst1":
			self.reader = RotationSystemTextReader(self.n,self.filepath,offset=1)
		elif self.filetype == "json0":
			self.reader = RotationSystemTextReader(self.n,self.filepath,offset=0,json_format=True)
		elif self.filetype == "json1":
			self.reader = RotationSystemTextReader(self.n,self.filepath,offset=1,json_format=True)
		else:
			raise Exception("Invalid Filetype: *."+self.filetype)

		print "read file:",self.filepath

		if self.automatic_output_writer:
			outpath = self.outfilepath+self.outfile_suffix+"."+self.outfiletype
			if self.outfiletype == "rsb0":
				self.writer = RotationSystemBinaryWriter(self.n,outpath,offset=0)
			elif self.outfiletype in ["rsb1","b08"]:
				self.writer = RotationSystemBinaryWriter(self.n,outpath,offset=1)
			elif self.outfiletype == "rst0":
				self.writer = RotationSystemTextWriter(self.n,outpath,offset=0)
			elif self.outfiletype in ["rst1","txt"]:
				self.writer = RotationSystemTextWriter(self.n,outpath,offset=1)
			elif self.outfiletype == 'json0':
				self.writer = RotationSystemTextWriter(self.n,outpath,offset=0,json_format=True)
			elif self.outfiletype == 'json1':
				self.writer = RotationSystemTextWriter(self.n,outpath,offset=1,json_format=True)
			else:
				raise Exception("Invalid Filetype: *."+self.outfiletype)

			print "write file:",outpath


	def action(self):
		self._init_files()
		self.count = 0
		self.show = 1

		starttime = datetime.now()

		print self.timestamp(),"loop started"

		for rs in self.reader.read_all():
			if self.count == self.show:
				if self.show < 1000:
					self.show = min(1000,2*self.show)
				else:
					self.show += 1000
				print self.timestamp(),self._progress_text()

			if (not self.from_ or self.from_ <= self.count) and (not self.to_ or self.count < self.to_):
				self._action_inner(rs)

			self.count += 1

		print self.timestamp(),self._progress_text()
		print self.timestamp(),"loop done ( time diff:",str(datetime.now()-starttime),")"
		self._action_end()

	def _progress_text(self): 
		return "** count: "+str(self.count)+" **"

	def timestamp(self): 
		return "["+str(datetime.now())+"]"