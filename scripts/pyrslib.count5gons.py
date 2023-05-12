#!/usr/bin/python2
# author: Manfred Scheucher (2016-2023)

from pyrslib import BasicScript

class UnifyRSScript(BasicScript.BasicScript): 

	def __init__(self):
		super(UnifyRSScript,self).__init__()
		self.rs_list = set()
		self.outfile_suffix = ".no5gon"
		self.stats = dict()
		self.ct = 0

	def _print_usage_info(self,rs):
		print "description:"
		print "\tthis script can be used to filter rotation systems that do not have convex n=5 sub rs"
		print "parameters:"
		print "\tjustcrossings (default 0)\t - just test crossing maximality"

	def _action_inner(self,rs):
		count = 0
		for sub_rs in rs.enumerate_sub_rotation_systems(5):
			if sub_rs.count_crossings() == 5: 
				count += 1
				break

		if count == 0:
			self.writer.write(rs)
			self.ct += 1
	

	def _progress_text(self): 
		return str(self.ct)+"/"+str(self.count)

	def _action_end(self): 
		print "stats:",self.ct,"of",self.count,"do not contain c5g."

if __name__ == "__main__": UnifyRSScript().action()
