#!/usr/bin/python2
# author: Manfred Scheucher (2016-2023)

from pyrslib import BasicScript

class UnifyRSScript(BasicScript.BasicScript): 

	def __init__(self):
		super(UnifyRSScript,self).__init__()
		self.rs_list = set()
		self.outfile_suffix = ".crossmin"
		self.stats = dict()
		self.split = int(self.arguments.get("split",0))
		self.splitfiles = {}
		self.enumerate = int(self.arguments.get("enumerate",0))

	def _print_usage_info(self,rs):
		print "description:"
		print "\tthis script can be used to count (enumerate) the number of crossings"
		print "parameters:"
		print "\tenumerate (default 0)\t- if all crossings should be enumerated"

	def _action_inner(self,rs):
		ct = rs.count_crossings()
		if ct not in self.stats:
			self.stats[ct] = 0
		print self.count,"->",ct

		#if ct == {4:0,5:1,6:3,7:9,8:18,9:36}[self.n]:
		#	self.writer.write(rs)
		
		self.stats[ct] += 1
		if self.DEBUG: print "[D] rs",self.count,"has",ct,"crossings"
		if self.enumerate:
			ct = 0
			print "rotation system #",self.count
			for cr in rs.enumerate_crossings():
				ct+=1
				print "- crossing #",ct,":",cr
			print

	def _action_end(self): 
		print "stats:"
		print "count\toccurrences"
		for i in sorted(self.stats):
			print i,"\t",self.stats[i]

if __name__ == "__main__": UnifyRSScript().action()
