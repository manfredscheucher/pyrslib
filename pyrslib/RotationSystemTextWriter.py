# author: Manfred Scheucher (2016-2023)

from FileWriter import FileWriter

class RotationSystemTextWriter(FileWriter):
	def __init__(self,n,filepath,always_flush=False,lazy_open=True,offset=0,json_format=False):
		super(RotationSystemTextWriter,self).__init__(n,filepath,always_flush,lazy_open,offset)
		self.json_format = json_format
		self.offset = offset

	def _write_next(self,rs):
		if self.json_format:
			s = rs.to_json_string(offset=self.offset)
			#s = "[["+"],[".join(",".join(str(x) for x in line) for line in self.orientations)+"]]"
		else:
			s = str(rs.n)+"\n"+rs.to_string(offset=self.offset)
			#s = str(rs.n)+"\n"+'\n'.join(' '.join(str(x+self.index0) for x in line) for line in rs.orientations)
		self.f.write(s+'\n')
