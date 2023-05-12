#!/usr/bin/python2
# author: Manfred Scheucher (2016-2023)

from pyrslib import BasicScript
from itertools import *

class UnifyRSScript(BasicScript.BasicScript): 

	def __init__(self):
		super(UnifyRSScript,self).__init__()
		self.rs_list = set()
		self.outfile_suffix = ".no3crf"
		self.stats = dict()
		self.enumerate = int(self.arguments.get("enumerate",0))

	def _print_usage_info(self,rs):
		print "description:"
		print "\tthis script can be used to count (enumerate) the number of crossings"
		print "parameters:"
		print "\tenumerate (default 0)\t- if all crossings should be enumerated"

	def _action_inner(self,rs):
		crossing_pairs = list(rs.enumerate_crossing_pairs())
		crossings_on = dict()
		for (a,b) in crossing_pairs:
			assert(a<b)
			assert(a[0]<a[1])
			assert(b[0]<b[1])
			if a not in crossings_on: crossings_on[a] = []
			if b not in crossings_on: crossings_on[b] = []
			crossings_on[a].append(b)
			crossings_on[b].append(a)
		
		found_triple = 0
		for a in crossings_on:
			for b,c in combinations(crossings_on[a],2):
				if c in crossings_on[b]:
					found_triple += 1
					break
			if found_triple: break

		if found_triple not in self.stats: self.stats[found_triple] = 0
		self.stats[found_triple] += 1 
		
		if not found_triple:
			print self.count,"has no triple"
			self.writer.write(rs)

		#print crossing_pairs


	def _action_end(self): 
		print "stats:"
		print "count\toccurrences"
		for i in sorted(self.stats):
			print i,"\t",self.stats[i]

if __name__ == "__main__": UnifyRSScript().action()
