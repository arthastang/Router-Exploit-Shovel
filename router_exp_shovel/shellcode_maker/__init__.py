#!/usr/bin/python3

import sys
sys.path.append("..")
from capstone import *
from capstone.mips import *
import yaml

class Shellcode_Maker():
	def __init__(self, **kwargs):
		self.shellcodeNum = kwargs['shellcodeNum']
		
	def getEncodeShellcode(self):
		shellFile = open('databases/shellcodes/shellcode'+str(self.shellcodeNum)+'.yaml','r')
		shellcode = yaml.safe_load(shellFile)
		return shellcode['shellcode']
			

