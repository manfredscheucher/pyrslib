#!/usr/bin/python2
# author: Manfred Scheucher (2016-2023)

from pyrslib import BasicScript,RotationSystem,ConvexityTest
from copy import *
from itertools import *
from sys import *



forbidden5orientations = [[1,2,3,4],[0,2,3,4],[0,3,1,4],[0,4,2,1],[0,3,1,2]]
forbidden5str = RotationSystem.RotationSystem(5,forbidden5orientations).to_string()


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
			valid2 = True
			for sub_rs in rs2.enumerate_sub_rotation_systems(5):
				sub_rs = sub_rs.calculate_lexmin()
				if sub_rs.orientations == forbidden5orientations:
					valid2 = False
					break
			if valid2: 
				yield rs2







class UnifyRSScript(BasicScript.BasicScript): 

	def __init__(self):
		super(UnifyRSScript,self).__init__()
		self.rs_list = set()
		self.depth = int(self.arguments.get("depth",0))

		self.convex = int(self.arguments.get("convex",0))
		self.hconvex = int(self.arguments.get("hconvex",0))
		self.fconvex = int(self.arguments.get("fconvex",0))

		self.outfile_suffix = ".flip"
		self.outfile_suffix += "_fconvex" if self.fconvex else ("_hconvex" if self.hconvex else ("_convex" if self.convex else ""))


	def _print_usage_info(self,rs):
		print "description:"
		print "\tscript can be used to compute the flip graph"
		print "parameters:"
		print "\tdepth (default 0)\t- depth 0 = recursive, depth 1 = just neighbors, depth 2 = neighbors of neighbors..."
		print "\tconvex (default 0)\t- filter convex"
		print "\thconvex (default 0)\t- filter h-convex"
		print "\tfconvex (default 0)\t- filter f-convex (necessary conditions, not sure if sufficient yet)"

	def _action_inner(self,rs):
		if self.fconvex:
			if not ConvexityTest.test_fconvex(rs,DEBUG=self.DEBUG>1): 
				return
		elif self.hconvex:
			if not ConvexityTest.test_hconvex(rs,DEBUG=self.DEBUG>1): 
				return
		elif self.convex:
			if not ConvexityTest.test_convex(rs,DEBUG=self.DEBUG>1): 
				return

		#self.DEBUG = 1
		rs = rs.calculate_lexmin()
		rsstr = rs.to_string()

		if rsstr not in self.rs_list:
			#assert(self.count == 0) # flipgraph conjectured to be connected

			self.rs_list.add(rsstr)
			self.writer.write(rs)

			todo = [rs]
			depth = 0
			while todo:
				depth += 1
				if self.depth != 0 and depth > self.depth: break

				rs1 = todo.pop()
				for rs2 in enum_all_flips(rs1):
					if self.fconvex:
						if not ConvexityTest.test_fconvex(rs2,DEBUG=self.DEBUG>1): 
							continue
					elif self.hconvex:
						if not ConvexityTest.test_hconvex(rs2,DEBUG=self.DEBUG>1): 
							continue
					elif self.convex:
						if not ConvexityTest.test_convex(rs2,DEBUG=self.DEBUG>1): 
							continue

					rs2 = rs2.calculate_lexmin()
					rsstr2 = rs2.to_string()

					if rsstr2 not in self.rs_list:
						self.rs_list.add(rsstr2)
						self.writer.write(rs2)
						todo.append(rs2)
						if self.DEBUG: 
							print self.count,"so far:",len(self.rs_list),"\r",
							stdout.flush()

			#if self.DEBUG: 
			print "[D] NEW connected component !!!",len(self.rs_list),"/",self.count
		else:
			if self.DEBUG: print "[D] already knew:",len(self.rs_list),"/",self.count

	def _progress_text(self): 
		return str(len(self.rs_list))+"/"+str(self.count)

	def _action_end(self): 
		print "number of rs:",len(self.rs_list),"/",self.count

if __name__ == "__main__": UnifyRSScript().action()
