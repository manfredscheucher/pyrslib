#!/usr/bin/python
"""
	pyotlib written and maintained
	by Manfred Scheucher (2016-2023)
"""


#from setuptools import setup
from distutils.core import setup
from distutils.extension import Extension

import os

# 2. configure scripts
scripts = ["scripts/"+f for f in os.listdir('./scripts') if f.endswith('.py') and f.startswith('pyrslib.')]
#scripts.append("scripts/pyrslib.rebuild.sh")
print "SCRIPTS:",scripts

# 3. setup
setup(
	name='pyrslib',
	version='0.0.1',
	author='Manfred Scheucher',
	packages=['pyrslib'],
	scripts=scripts,
)
 
