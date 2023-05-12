#!/usr/bin/python2
# author: Manfred Scheucher (2016-2023)

from pyrslib import BasicScript,RotationSystem
from copy import *
from itertools import *
from sys import *



forbidden5orientations = [[1,2,3,4],[0,2,3,4],[0,3,1,4],[0,4,2,1],[0,3,1,2]]
forbidden5str = RotationSystem.RotationSystem(5,forbidden5orientations).to_json_string()


def enum_all_flips(rs):
	n = rs.n
	k = n-1
	o = deepcopy(rs.orientations)

	for a,b,c in permutations(range(n),3):
		oa = o[a]
		ob = o[b]
		iab = oa.index(b)
		iac = oa.index(c)
		iba = ob.index(a)
		ibc = ob.index(c)
		if iac == ((iab+1)%k) and iba == ((ibc+1)%k):
			# valid flip
			o2 = deepcopy(o)
			o2[a][iab] = c
			o2[a][iac] = b
			o2[b][iba] = c
			o2[b][ibc] = a
			rs2 = RotationSystem.RotationSystem(n,o2)
			yield rs2







class UnifyRSScript(BasicScript.BasicScript): 

	def __init__(self):
		super(UnifyRSScript,self).__init__()
		self.rsstr_list = set()
		self.rs_map = dict()
		self.outfile_suffix = ".flip"


	def _print_usage_info(self,rs):
		print "description:"
		print "\tscript can be used to compute the flip graph"
		print "parameters:"

	def _action_inner(self,rs):
		#self.DEBUG = 1
		rs = rs.calculate_lexmin()
		rsstr = rs.to_json_string()

		if rsstr not in self.rsstr_list:
			#assert(self.count == 0) # flipgraph conjectured to be connected
			self.rsstr_list.add(rsstr)
			self.rs_map[rsstr] = rs
			self.writer.write(rs)


	def _progress_text(self): 
		return str(len(self.rsstr_list))+"/"+str(self.count)

	def _action_end(self):
		print "loaded",len(self.rsstr_list),"rotation systems"

		unvisited = list(self.rsstr_list)
		#unvisited.reverse()
		num_cc = 0
		while unvisited:
			num_cc += 1
			cc_size = 0
			rs0str = unvisited.pop()
			rs0 = self.rs_map[rs0str]
			todo = [(rs0str,rs0)]
			while todo:
				cc_size += 1
				if self.DEBUG: 
					print "cc size far:",cc_size,"\r",
					stdout.flush()

				rs1str,rs1 = todo.pop()
				assert(rs1str == rs1.to_json_string())
				for rs2 in enum_all_flips(rs1):
					rs2 = rs2.calculate_lexmin()
					rs2str = rs2.to_json_string()

					if rs2str in unvisited:
						unvisited.remove(rs2str)
						todo.append((rs2str,rs2))

			print "found connected component of size",cc_size,"@",rs0str.replace("\n",",")
		print "total number of connected components:",num_cc

if __name__ == "__main__": UnifyRSScript().action()
