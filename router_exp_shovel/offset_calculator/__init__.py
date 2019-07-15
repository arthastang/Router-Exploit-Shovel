#!/usr/bin/python3

import sys
sys.path.append("..")
import struct
import pickle

class Offset_Calculator():
	def __init__(self, **kwargs):
		#kwargs later
		#Load base address
		self.loadBase = 0x400000
		#stack overflow point
		#addiu $a1,$sp,xxx
		self.overflowP = ['27','a5']
		#contrlReg point
		#sw $ra,xxx($sp)
		self.contrlRegP = ['af','bf']
		#Offset overflow point
		self.overflowO = 0
		#Offset contrlReg point
		self.contrlRegO = 0

		self.binaryPath = kwargs['binaryPath']
		self.overflowAddress = kwargs['overflowAddress']

	def getGeneratePadding(self):

		#read binaryfile
		binary = open(self.binaryPath,"rb")
		
		#find stack overflow point
		#Branch delay slot
		binary.seek(self.overflowAddress - self.loadBase + 0x4)
		opStr = binary.read(2)
		#print(str(opStr))
		op = ["{:02x}".format(c) for c in opStr]
		#print(op)

		if self.overflowP == op:
			s = binary.read(2)
			l = ["{:02x}".format(c) for c in s]
			self.overflowO = int(l[0],16) + int(l[1],16)
			print("\033[1;;34m[INFO]\033[0m Find stack overflow point offset " + hex(self.overflowO))
		
		#Roll up
		count = 0
		while True:
			count += 0x4		
			binary.seek(self.overflowAddress - self.loadBase - count)
			opStr = binary.read(2)
			op = ["{:02x}".format(c) for c in opStr]
			if self.overflowP == op:
				s = binary.read(2)
				l = ["{:02x}".format(c) for c in s]
				self.overflowO = int(l[0],16) + int(l[1],16)
				print("\033[1;;34m[INFO]\033[0m Find stack overflow point offset " + hex(self.overflowO))
				break
	
		#find contrlReg point
		#Roll up
		count = 0
		while True:
			count += 0x4		
			binary.seek(self.overflowAddress - self.loadBase - count)
			opStr = binary.read(2)
			op = ["{:02x}".format(c) for c in opStr]
			if self.contrlRegP == op:
				s = binary.read(2)
				l = ["{:02x}".format(c) for c in s]
				self.contrlRegO = int(l[0],16) + int(l[1],16)
				print("\033[1;;34m[INFO]\033[0m Find contrlReg point offset " + hex(self.contrlRegO))
				break		
	
		#computing the Control offset for generate padding
		#for gadg
		paddingO = self.contrlRegO - self.overflowO -0x4
		binary.close()
		return paddingO
