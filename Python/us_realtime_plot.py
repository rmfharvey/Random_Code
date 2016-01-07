import sys, serial, argparse
import numpy as np
from time import sleep
from collections import deque

import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import math 

def is_number(st):
	try:
		float(st)
		return True
	except ValueError:
		return False
	except:
		print("ERROR in is_number()")
		sys.exit(0)		
	
def line_to_int(utf8_line):
	value = 0
	try:
		for n in utf8_line:
			if is_number(n):
				value = 10*value +int(n)
		return value
	except:
		print("line_to_int failed.\n")
		return -1

temp_data = 0  

class AnalogPlot:
	def __init__(self, strPort, maxLen):
		self.ser = serial.Serial(port=strPort, baudrate=115200)
		print('Reading from serial port %s...'%self.ser.name)
		print("HERE")
		self.ax = deque([0.0]*maxLen)
		self.ay = deque([0.0]*maxLen)
		self.maxLen = maxLen
		print("HERE")
	def addToBuf(self, buf, val):
		if len(buf) < self.maxLen:
			buf.append(val)
		else:
			buf.pop()
			buf.appendleft(val)
	def add(self, data):
		assert(len(data) == 2)
		self.addToBuf(self.ax, data[0])
		self.addToBuf(self.ay, data[1])
	def update(self, frameNum, a0, a1):
		global temp_data
		
		try:
			data = [float(line_to_int(self.ser.readline().decode('utf-8'))), 0]
			if(len(data) == 2):
				self.add(data)
				a0.set_data(range(self.maxLen), self.ax)
				a1.set_data(range(self.maxLen), self.ay)
		except KeyboardInterrupt:
			print('Exiting...')
		
		return a0, 
	def close(self):
		self.ser.flush()
		self.ser.close()    

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="LDR serial")
	parser.add_argument('--port', dest='port', required=True)
	args = parser.parse_args()
	strPort = args.port
	
	
	#strPort = input("COM Port:  ")
	#print("HERE %s\n"%strPort)
	#strPort = int(strPort)-1
	#print("HERE\n")
	analogPlot = AnalogPlot(strPort, 100)
	
	print('Plotting data...')
	
	fig = plt.figure()
	ax = plt.axes(xlim=(0, 100), ylim=(0, 1023))
	a0, = ax.plot([], [])
	a1, = ax.plot([], [])
	anim = animation.FuncAnimation(fig, analogPlot.update, 
								fargs=(a0, a1), 
								interval=50)
	
	plt.show()
	analogPlot.close()
	
	print('Exiting...')
  
