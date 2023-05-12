# author: Manfred Scheucher (2016-2023)

class ArgumentReader(object):
	
	def __init__(self, arguments):
		self.d = dict()
		l = len(arguments)
		for i in range(1,l-1,2):
			self.d[arguments[i]] = arguments[i+1] 

	def get(self, name, default=None):
		if name in self.d: return self.d[name]
		if default != None: return default		
		raise Exception("No Parameter \""+name+"\" found!")
