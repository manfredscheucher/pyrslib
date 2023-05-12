#!/usr/bin/python2
# author: Manfred Scheucher (2016-2023)

from pyrslib import BasicScript

from pyrslib.RotationSystemTextReader import RotationSystemTextReader
from pyrslib.RotationSystemBinaryReader import RotationSystemBinaryReader
from pyrslib.RotationSystemTextWriter import RotationSystemTextWriter
from pyrslib.RotationSystemBinaryWriter import RotationSystemBinaryWriter

all5jsonstrs = [
	'[[1,2,3,4],[0,2,3,4],[0,1,3,4],[0,1,2,4],[0,1,2,3]]',
	'[[1,2,3,4],[0,2,3,4],[0,1,3,4],[0,1,4,2],[0,1,3,2]]',
	'[[1,2,3,4],[0,2,3,4],[0,1,4,3],[0,1,2,4],[0,1,3,2]]',
	'[[1,2,3,4],[0,2,4,3],[0,1,3,4],[0,1,4,2],[0,3,1,2]]',
	'[[1,2,3,4],[0,3,4,2],[0,1,4,3],[0,2,4,1],[0,3,2,1]]',
]

class UnifyRSScript(BasicScript.BasicScript): 

	def __init__(self):
		super(UnifyRSScript,self).__init__()
		self.k = int(self.arguments.get("k",self.n-1))
		self.outfile_suffix = ".subrs"+str(self.k)
		self.calculate_lexmin = int(self.arguments.get("calculate_lexmin",1))
		
		self.global_sub_rs_list = set()

		self.matrix = []

		# cf. BasicScript.py
		outpath = self.outfilepath+self.outfile_suffix+"."+self.outfiletype
		if self.outfiletype == "rsb0":
			self.writer = RotationSystemBinaryWriter(self.k,outpath,offset=0)
		elif self.outfiletype in ["rsb1","b08"]:
			self.writer = RotationSystemBinaryWriter(self.k,outpath,offset=1)
		elif self.outfiletype == "rst0":
			self.writer = RotationSystemTextWriter(self.k,outpath,offset=0)
		elif self.outfiletype in ["rst1","txt"]:
			self.writer = RotationSystemTextWriter(self.k,outpath,offset=1)
		else:
			raise Exception("Invalid Filetype: *."+self.outfiletype)


	def _print_usage_info(self,rs):
		print "description:"
		print "\tthis script can be used to enumerate all subrotation systems"
		print "parameters:"
		print "\tk (default n-1)\t- size of sub rotation systems"
		print "\tcalculate_lexmin (default: 1)"

	def _action_inner(self,rs):
		sub_rs_list = {}
		for sub_rs in rs.enumerate_sub_rotation_systems(self.k):
			if self.calculate_lexmin: sub_rs = sub_rs.calculate_lexmin()
			sub_rs_str = sub_rs.to_json_string()
			if sub_rs_str not in sub_rs_list:
				sub_rs_list[sub_rs_str] = 0
				if sub_rs_str not in self.global_sub_rs_list:
					self.global_sub_rs_list.add(sub_rs_str)
					self.writer.write(sub_rs)

			sub_rs_list[sub_rs_str] += 1
			

		print "======= rs #",self.count,"========="
		print rs.to_json_string()
		total = 0


		for sub_rs_str in sub_rs_list:
			if sub_rs_list[sub_rs_str] >= 0: total += 1 
			print sub_rs_list[sub_rs_str],"x",sub_rs_str

		print "total:",total
	
		if self.k == 5:
			row = [sub_rs_list[s] if s in sub_rs_list else 0 for s in all5jsonstrs]
			print row
			self.matrix.append(row)

		print 
		print


	def _action_end(self): 
		print "overall: found",len(self.global_sub_rs_list),"subrotationsystems"
		#print(self.matrix)
		None

if __name__ == "__main__": UnifyRSScript().action()
