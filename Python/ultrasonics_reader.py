# 	ultrasonics_reader.py
#	Ross Harvey 	
# 	8/6/15

import serial
import sys
import csv
import string
import time
from math import *
import datetime
import shutil
import os
from ctypes import *
import ultrasonics

#sys.argv.append('-m') 		#for .exe build

print("\nPython Version %s\n"
	  "Run with arg -h (i.e. python %s -h) to see help menu.\n"%(sys.version,sys.argv[0]))

PERIOD = 0
AVGNUM = 10000

class sysarg_t:
	def __init__(self):
		self.VERBOSE = False
		self.LOGGING = False
		self.MONITOR = False
		self.HELP = False
		
def is_number(st):
	try:
		float(st)
		return True
	except ValueError:
		return False
	except:
		print("ERROR in function is_number()")
		sys.exit(0)	

def readline_blocking():
	line = ""
	while not line:
		line = ser.readline()
	return line	
	
def stdev(arr, avg):
	temp=0
	arrSize = len(arr)
	for i in range(0,arrSize):
		temp += (arr[i] - avg)**2
	return sqrt(temp/arrSize)

def logData():
	adcAvg = 0		
	countAvg = 0
	adcArr = []
	countArr = []
	adcValue=0
	countValue=0
	global file
	readCount = 0
	numData = int(input("Enter number of data points: "))
	while(readCount<numData):
		readCount += 1
		
		for i in range(0,2):
			data = 0
			data = readline_blocking()
			data = data[:-2]
			packet = ultrasonics.Packet(data, verbose=False)
			if(packet.isADC):	
				adcValue = packet.val
				adcAvg += packet.val
				adcArr.append(packet.val)
			if(packet.isCount):	
				countValue = packet.val
				countAvg += packet.val
				countArr.append(packet.val)
		print("Reads:\t%d    "%(readCount), end="\r")
		
		with open(outfile, 'a', newline='') as file:
			output = csv.writer(file)
			output.writerow([readCount, adcValue, countValue])
		file.close()
	
	adcAvg /= numData
	countAvg /= numData
	
	print("Total Reads: %d\n"%numData)
	print("Averages\nADC:\t\t%.3fV\nCounter:\t%.0f"%(adcAvg,countAvg))
	print()
	print("Standard Deviations\nADC:\t\t%.3fmV\nCounter:\t%.3f"%(1000*stdev(adcArr, adcAvg), stdev(countArr, countAvg)))
	print("\nRange\nADC:\t\t%.2fmV\t[%.3f, %.3f]\nCounter:\t%.0f\t[%.0f, %.0f]"%(1000*(max(adcArr)-min(adcArr)),min(adcArr),max(adcArr),max(countArr)-min(countArr),min(countArr),max(countArr)))
	
def displayPacket():
	adcAvg = 0		
	countAvg = 0
	adcArr = []
	countArr = []
	adcValue=0
	countValue=0
	for i in range(0,2):
		data = readline_blocking()
		data = data[:-2]
		packet = ultrasonics.Packet(data, verbose=False)
		if(packet.isADC):	
			adcValue = packet.val
		if(packet.isCount):	
			countValue = packet.val
	print("ADC Value: %.3fv	Counter: %d      "%(adcValue,countValue), end='\r')
	
	
#### System Arguments ###################################################################	
ARG = sysarg_t()
if "-h" in sys.argv:
	ARG.HELP = True
if "-v" in sys.argv:
	ARG.VERBOSE = True
	print("\n")
	print("Python Version %s\n"%sys.version)
	print("Run with arg -h (i.e. python %s -h) to see help menu.\n"%sys.argv[0])
if "-l" in sys.argv:
	ARG.LOGGING = True
	ARG.MONITOR = False
if "-m" in sys.argv:
	ARG.MONITOR = True
	ARG.LOGGING = False

#########################################################################################


if ARG.HELP:
	print("\nHelp Menu\n"
		  "----------------------------------------------------------------------\n"
		  "Optional Arguments:\n"
		  "  -v\tVerbose Mode.  Enables extra console output.\n"
		  "  -l\tLogging Mode.  Write data to a csv file and run statistical analyses.\n"
		  "  -m\tMonitor Mode.  Display appropriate values on console output.\n"
		  "  -h\tHelp menu.     But you already knew that...\n"
		  )
	sys.exit(0)

#	Start Serial Connection
COM_PORT = 16
#COM_PORT = int(input("Enter COM port Number: "))
print()
try:
	ser = serial.Serial((COM_PORT-1),115200,timeout = 0.01)
	print ("Connection started on %s\n"
		   "----------------------------------------------------------------------\n"%ser.name)
except:
	print("CONNECTION FAILED.  EXITING...")
	sys.exit(0)

###	Create directory and csv file
try:
	if ARG.LOGGING:
		cur_path = os.getcwd()
		testfile_dir = "Test Results"
		testfile_path = cur_path + "\\" + testfile_dir
	
		if not(os.path.exists(testfile_path)):	# Make new directory if necessary
			os.mkdir(testfile_path)
			time.sleep(0.01)
		os.chdir(testfile_path)
		time.sleep(0.01)
	
		outfile = input("Enter filename: ")
		
		if(testfile_path == str(os.getcwd())):	# If directory change succeeded
			print("\nTest results stored in %s\n"%str(os.getcwd()))
		elif LOGGING:
			print("\nchdir() FAILED. TEST RESULTS DIRECTORY IS UNDEFINED...\n")
	
		ts = time.strftime("_%m-%d-%y_%H-%M-%S")
		outfile = outfile + ts + ".csv"
except:
	print("\nERROR!  CSV file creation failed.\n")
	
# 	Start main routine
if __name__ == '__main__':
	try:
		data = readline_blocking()
		if ARG.LOGGING:
			logData()	
		elif ARG.MONITOR:
			while True:
				displayPacket()
	except:
		print("ERROR!  EXITING...")
	finally:
		if (cur_path != str(os.getcwd())):
			os.chdir(cur_path)
		else:
			print("\nFailed to move back to original directory :(")
		if(ser.isOpen()):
			ser.close()
		sys.exit(0)			