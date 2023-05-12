#!/usr/bin/python2
# author: Manfred Scheucher (2016-2023)

from pyrslib import BasicScript
from itertools import combinations, permutations

class UnifyRSScript(BasicScript.BasicScript): 

	def __init__(self):
		super(UnifyRSScript,self).__init__()
		self.rs_list = set()
		self.outfile_suffix = ".realizable"
		self.stats = set()
		self.ct = 0

	def _print_usage_info(self,rs):
		print "description:"
		print "\tthis script can be used to count (enumerate) the number of crossings"
		print "parameters:"
		print "\tenumerate (default 0)\t- if all crossings should be enumerated"

	def _action_inner(self,rs):

		crn = rs.count_crossings()
		if self.n == 6 and crn < 8:
			print "crossings:",crn
			print "SKIP: "

		val = 0
		stat = dict()
		goodD = set()
		for (a,b,c) in combinations(range(rs.n),3):		
			A = []
			B = []
			C = []
			for d in range(rs.n):
				if d in [a,b,c]: continue

				sub_rs = rs.sub_rotation_system_from_permutation([a,b,d,c])
				if sub_rs.count_crossings() != 0 :
					for cr,perm in sub_rs.enumerate_crossings(return_perm=True):
						if perm == [0,1,2,3] or perm == [0,3,2,1]:
							A.append(d)
				sub_rs = rs.sub_rotation_system_from_permutation([b,c,d,a])
				if sub_rs.count_crossings() != 0 :
					for cr,perm in sub_rs.enumerate_crossings(return_perm=True):
						if perm == [0,1,2,3] or perm == [0,3,2,1]:
							B.append(d)
				sub_rs = rs.sub_rotation_system_from_permutation([c,a,d,b])
				if sub_rs.count_crossings() != 0 :
					for cr,perm in sub_rs.enumerate_crossings(return_perm=True):
						if perm == [0,1,2,3] or perm == [0,3,2,1]:
							C.append(d)

			print "rs #",self.count,":","a,b,c",a,b,c,"->",A,B,C
			if len(A) == 2 or len(B) == 2 or len(C) == 2:
				if len(A) == 2: goodD |= set(A)
				if len(B) == 2: goodD |= set(B)
				if len(C) == 2: goodD |= set(C)
				val+=1
		
		print "crossings:",crn
		print "VAL",val,len(goodD)
		print 100*"-"
			
		self.stats.add((crn,val,len(goodD)))
		
#		self.ct += 1
#		if self.DEBUG: print self.timestamp(),"rs #",self.count,"does not contain 5 gon"
#		self.writer.write(rs)


	def _action_end(self): 
		print "stats:",self.ct,"of",self.count,"realizable."
		print "stats",self.stats


if __name__ == "__main__": UnifyRSScript().action()
