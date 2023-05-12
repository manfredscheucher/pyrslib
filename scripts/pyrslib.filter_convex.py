#!/usr/bin/python2
# author: Manfred Scheucher (2016-2023)

from pyrslib import BasicScript, RotationSystem, ConvexityTest

from pyrslib.RotationSystemTextReader import RotationSystemTextReader
from pyrslib.RotationSystemBinaryReader import RotationSystemBinaryReader
from pyrslib.RotationSystemTextWriter import RotationSystemTextWriter
from pyrslib.RotationSystemBinaryWriter import RotationSystemBinaryWriter

class UnifyRSScript(BasicScript.BasicScript): 

	def __init__(self):
		super(UnifyRSScript,self).__init__()
		self.convex = int(self.arguments.get("convex",1))
		self.hconvex = int(self.arguments.get("hconvex",0))
		self.fconvex = int(self.arguments.get("fconvex",0))

		if self.fconvex: self.hconvex = self.fconvex 
		if self.hconvex: self.convex = self.hconvex 

		self.complement = int(self.arguments.get("complement",0))


		if not self.complement:
			self.outfile_suffix = ".fconvex" if self.fconvex else (".hconvex" if self.hconvex else ".convex")
		else:
			self.outfile_suffix = ".notfconvex" if self.fconvex else (".nothconvex" if self.hconvex else ".notconvex")

		self.convex_count = 0


		
	def _print_usage_info(self,rs):
		print "description:"
		print "\tthis script can be used to enumerate all subrotation systems"
		print "parameters:"
		print "\tconvex (convex 0)\t- filter convex"
		print "\thconvex (default 0)\t- filter h-convex"
		print "\tfconvex (default 0)\t- filter f-convex (necessary conditions, not sure if sufficient yet)"
		print "\tcomplement (default 0)\t- filter complement, that is, obstructions"


	def _action_inner(self,rs):

		if self.fconvex:
			convex = ConvexityTest.test_fconvex(rs,DEBUG=self.DEBUG)
		elif self.hconvex:
			convex = ConvexityTest.test_hconvex(rs,DEBUG=self.DEBUG)
		else:
			convex = ConvexityTest.test_convex(rs,DEBUG=self.DEBUG)

		if convex:
			self.convex_count += 1
			if not self.complement:
				self.writer.write(rs)

		if not convex and self.complement:
			self.writer.write(rs)
		
		if self.DEBUG: print "so far:","fconvex" if self.fconvex else ("hconvex" if self.hconvex else "convex"),":",self.convex_count,"of",self.count

	def _action_end(self): 
		print "fconvex" if self.fconvex else ("hconvex" if self.hconvex else "convex"),":",self.convex_count,"of",self.count


if __name__ == "__main__": UnifyRSScript().action()
