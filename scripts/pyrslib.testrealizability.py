#!/usr/bin/python2
# author: Manfred Scheucher (2016-2023)

from pyrslib import BasicScript

class UnifyRSScript(BasicScript.BasicScript): 

	def __init__(self):
		super(UnifyRSScript,self).__init__()
		self.outfile_suffix = ".realizable"
		self.ct = 0
		self.DEBUG = 1

	def _print_usage_info(self,rs):
		print "description:"
		print "\tthis script can be used to test if a rotation system is realizable"

	def _action_inner(self,rs):
		for sub_rs in rs.enumerate_sub_rotation_systems(5):
			if sub_rs.count_crossings() == 5:
				sub_rs = sub_rs.calculate_lexmin()
				if sub_rs.orientations[-2][1] == 4:
					if self.DEBUG: print self.timestamp(),"rs #",self.count,"not realizable"
					return

		self.ct += 1
		if self.DEBUG: print self.timestamp(),"rs #",self.count,"does not contain 5 gon"
		self.writer.write(rs)


	def _action_end(self): 
		print "stats:",self.ct,"of",self.count,"realizable."

if __name__ == "__main__": UnifyRSScript().action()
