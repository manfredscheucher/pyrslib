# author: Manfred Scheucher (2016-2023)

from itertools import combinations, permutations

def _cannonical_permutation(perm):
	k0 = perm.index(min(perm))
	return perm[k0:]+perm[:k0]

class RotationSystem(object):
	def __init__(self,n,orientations):
		self.n = n
		self.orientations = orientations

	def to_string(self,offset=0):
		return "\n".join(" ".join(str(x+offset) for x in line) for line in self.orientations)
	
	def to_json_string(self,offset=0):
		return "[["+"],[".join(",".join(str(x+offset) for x in line) for line in self.orientations)+"]]"

	def is_valid(self):
		for i in range(self.n): 
			if sorted(self.orientations[i]+[i]) != range(self.n):
				return False
		return True
			
	def four_indices_have_crossing(self):
		assert(self.n == 4) # TODO: check if lexmin labeling (and speedup)!
		def _count_inversions(p):
			return len([(a,b) for (a,b) in combinations(range(3),2) if p[a]>p[b]])
		inversertion = [l for l in self.orientations if (_count_inversions(l) % 2) == 0]
		return len(inversertion) != 2

	def calculate_mirrored(self):
		return RotationSystem(self.n,[_cannonical_permutation(list(reversed(line))) for line in self.orientations])

	def calculate_lexmin(self,return_perm=False):
		self_mirrored = self.calculate_mirrored()
		rs1 = self
		perm1 = range(self.n)
		rs1str = rs1.to_string()
		for (a,b) in permutations(range(self.n),2):
			line = self.orientations[a]
			k0 = line.index(b)
			perm2 = [a,b]+line[k0+1:]+line[:k0]
			rs2 = self.sub_rotation_system_from_permutation(perm2)
			rs2str = rs2.to_string()
			assert(rs2.orientations[0] == range(1,self.n)) 

			if rs2str < rs1str:
				rs1,rs1str,perm1 = rs2,rs2str,perm2

			perm2 = [a,b]+list(reversed(line[k0+1:]+line[:k0]))
			rs2 = self_mirrored.sub_rotation_system_from_permutation(perm2)
			rs2str = rs2.to_string()
			assert(rs2.orientations[0] == range(1,self.n)) 

			if rs2str < rs1str: 
				rs1,rs1str,perm1 = rs2,rs2str,perm2
		return (rs1,perm1) if return_perm else rs1

	def enumerate_sub_rotation_systems(self,k,return_perm=False):
		for perm in combinations(range(self.n),k):
			sub_rs = self.sub_rotation_system_from_permutation(perm)
			yield (sub_rs,perm) if return_perm else sub_rs

	def sub_rotation_system_from_permutation(self,perm):
		sub_orientations = [_cannonical_permutation([perm.index(b) for b in self.orientations[a] if b in perm]) for a in perm]		
		return RotationSystem(len(perm),sub_orientations)

	def count_crossings(self,maxcount=None):
		ct = 0
		for cr in self.enumerate_crossings():
			ct += 1
			if maxcount!=None and ct > maxcount:
				break # already counted enough
		if self.n > 4: assert(ct > 0)
		return ct

	def enumerate_crossings(self,return_perm=False):
		for sub_rs,perm in self.enumerate_sub_rotation_systems(4,return_perm=True):
			sub_rs_lexmin,perm_lexmin = sub_rs.calculate_lexmin(return_perm=True)
			if sub_rs_lexmin.four_indices_have_crossing(): 
				yield (perm,perm_lexmin) if return_perm else perm

	def enumerate_crossing_pairs(self):
		for cr,perm in self.enumerate_crossings(return_perm=True):
			a,b = cr[perm[0]],cr[perm[2]]
			c,d = cr[perm[1]],cr[perm[3]]
			if a > b: a,b = b,a
			if c > d: c,d = d,c
			ab = (a,b)
			cd = (c,d)
			if ab > cd: ab,cd = cd,ab
			yield (ab,cd)