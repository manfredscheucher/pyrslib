# author: Manfred Scheucher (2016-2023)

from RotationSystem import RotationSystem
from FileReader import FileReader

from ast import literal_eval


class RotationSystemTextReader(FileReader):
	def __init__(self,n,filepath,offset=0,NATURAL_LABELING=True,json_format=False):
		super(RotationSystemTextReader,self).__init__(n,filepath,offset)
		self.NATURAL_LABELING = NATURAL_LABELING
		self.json_format = json_format

	def read_next(self):
		
		if self.json_format:
			l = self.f.readline()
			if l == "": return None # end of file reached
			orientations = literal_eval(l)

		else:
			orientations = []

			for i in range(self.n):
				l = self.f.readline()
				if i == 0:
					if l == "": return None # end of file reached
					n = int(l)
					assert(n == self.n)
					l = self.f.readline()
					first_entry = int(l.split()[0])-self.index0
					if not self.NATURAL_LABELING: assert(first_entry==1)

				orientations.append([int(x)-self.index0 for x in l.split()])

		return RotationSystem(self.n, orientations)
