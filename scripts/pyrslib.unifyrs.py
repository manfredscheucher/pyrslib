#!/usr/bin/python2
# author: Manfred Scheucher (2016-2023)

from pyrslib import BasicScript
from copy import *

class UnifyRSScript(BasicScript.BasicScript): 

	def __init__(self):
		super(UnifyRSScript,self).__init__()
		#self.rs_list = set()
		self.rs_list = dict()
		self.outfile_suffix = ".unified"
		self.calculate_lexmin = int(self.arguments.get("calculate_lexmin",1))
		self.show_permutation = int(self.arguments.get("show_permutation",0))

	def _print_usage_info(self,rs):
		print "description:"
		print "\tscript can be used to filter duplicates"
		print "parameters:"
		print "\tcalculate_lexmin (default: 1)"
		print "\tshow permutation (default: 0)"

	def _action_inner(self,rs0):
		rs = copy(rs0)
		if self.calculate_lexmin: 
			rs,perm = rs.calculate_lexmin(return_perm=True)
			if self.show_permutation:
				print 80*"-"
				print "input"
				print rs0.to_string()
				print "perm"
				print perm
				print "output"
				print rs.to_string()
				print 80*"-"

		rsstr = rs.to_string()
		if rsstr not in self.rs_list:
			#self.rs_list.add(rsstr)
			self.rs_list[rsstr] = self.count
			self.writer.write(rs)
			if self.DEBUG: print "[D] new rs:",len(self.rs_list),"/",self.count
			if self.DEBUG: print rs.to_json_string()
		else:
			#if self.DEBUG: print "[D] already knew:",len(self.rs_list),"/",self.count
			if self.DEBUG: print "[D] duplicate spotted: #",self.count,"=",self.rs_list[rsstr]
			

	def _progress_text(self): 
		return str(len(self.rs_list))+"/"+str(self.count)

	def _action_end(self): 
		if self.DEBUG: print self.rs_list
		print "number of rs:",len(self.rs_list),"/",self.count
	

if __name__ == "__main__": UnifyRSScript().action()
