#!/usr/bin/python2
# author: Manfred Scheucher (2016-2023)

from pyrslib import BasicScript
from itertools import *

class UnifyRSScript(BasicScript.BasicScript): 

	def __init__(self):
		super(UnifyRSScript,self).__init__()
		self.outfile_suffix = ".no_tverberg"
		self.stats = dict()

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
			
		assert(self.n == 10)
		found_triple = 0
		for a in crossings_on:
			for b,c1 in permutations(crossings_on[a],2):
				for c2 in crossings_on[b]:
					if set(c1) & set(c2):
						c3 = tuple(sorted([c for c in c1+c2 if c not in c1 or c not in c2]))
						crossings_on_c = set(crossings_on[c1]+crossings_on[c2]+crossings_on[c3])
						for d1 in crossings_on[a]:
							for d2 in crossings_on[b]:
								if set(d1) & set(d2):
									for d3 in crossings_on_c:
										if set(d1) & set(d3) and set(d2) & set(d3):
											found_triple += 1
											break
									if found_triple: break
							if found_triple: break
						if found_triple: break
				if found_triple: break
			if found_triple: break

		if found_triple not in self.stats: self.stats[found_triple] = 0
		self.stats[found_triple] += 1 
		
		if not found_triple:
			print self.count,"has no tverberg"
			self.writer.write(rs)

		#print crossing_pairs


	def _action_end(self): 
		print "stats:"
		print "count\toccurrences"
		for i in sorted(self.stats):
			print i,"\t",self.stats[i]

if __name__ == "__main__": UnifyRSScript().action()
