import string

class Packet:
	isADC = False
	isCount = False
	mask = None		
	rawVal = None	# hex string to be formatted
	val = None
	
	def __init__(self, initVal, verbose=False):
		self.rawVal=initVal
		self.verbose = verbose
		self.setMask()
		self.setVal()
	
	def setMask(self):
		self.mask = self.formatVal(self.rawVal[0:2])
		if(self.mask==0xA0):
			self.isADC = True
			self.isCount = False
		elif(self.mask==0xB0):
			self.isADC = False
			self.isCount = True
		else:
			self.isADC = False
			self.isCount = False
			
	def setVal(self):
		if(self.isADC):
			self.val = (self.formatVal(self.rawVal[2:4])) + (self.formatVal(self.rawVal[4:8]))/10000.0
		elif(self.isCount):
			self.val = self.formatVal(self.rawVal[2:8])
		else:
			self.val = None
			
	def showParams(self):
		if self.verbose:
			print("isADC:\t\t%s\nisCount:\t%s\nMask:\t\t%s\nrawVal:\t\t%s\nval:\t\t%s\n"%(self.isADC, self.isCount, self.mask, self.rawVal, self.val))
		else:
			if(self.isADC):
				#print("ADC Packet")
				print("ADC Value:\t%.4fv"%self.val)
			elif(self.isCount):
				#print("Counter Packet")
				print("Counter Value:\t%.0f"%self.val)
			else:
				print("NOT A VALID PACKET")
	
	def formatVal(self, data):		# takes a hex ASCII string and returns its int value
		frmtData = 0
		dataList = []
		for j in data:	
			dataList.append(self.ASCIItoInt(j))
		maxBytes = len(dataList)	
		for j in range(0,maxBytes):
			frmtData |= dataList[maxBytes-j-1]<<(4*j)
		return frmtData
	
	def ASCIItoInt(self, singleChar):	# converts a single ASCII char to int
		if(0x2F<singleChar<0x3A):
			return singleChar-0x30
		elif(0x60<singleChar<0x67):
			return singleChar-0x61+10
		elif(0x40<singleChar<0x47):
			return singleChar-0x41+10	
		else:
			return None
			
	def __exit__(self, *err):
		self.close()