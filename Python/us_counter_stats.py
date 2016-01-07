#us_counter_stats.py

import serial
import csv
import time
import string
import shutil
import os
import sys

print("here")

logCount = 0

sys.argv.append('-l') 		#add -m for .exe build

class sysarg_t:
	def __init__(self):
		self.VERBOSE = False
		self.LOGGING = False
		self.MONITOR = False
		self.HELP = False

print("\nPython Version %s\n"
	  "Run with arg -h (i.e. python %s -h) to see help menu.\n"%(sys.version,sys.argv[0]))

def is_number(st):
	try:
		float(st)
		return True
	except ValueError:
		return False
	except:
		print("ERROR in function is_number()")
		sys.exit(0)	
		
def log_data(data):
	global logCount
	logCount += 1
	with open(outfile, 'a', newline='') as file:
		output = csv.writer(file)
		output.writerow([logCount, data])
	

def readline_blocking():
	line = ""
	while not line:
		line = ser.readline()
	return line	
	
def stats(arr):
	temp=0
	average=0
	for num in arr:
		average+=num
	average /= len(arr)
	for i in arr:
		temp += (i-average)**2
	return (average, sqrt(temp/arrSize))
		
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

#### Help Menu ##########################################################################
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
#### Help Menu END #####################################################################	

#### COM Setup #########################################################################
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
#### COM Setup END #####################################################################

#### CSV and Directory #################################################################
try:
	if ARG.LOGGING:
		cur_path = os.getcwd()
		testfile_dir = "Counter Test Results"
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
#### CSV and Directory END #############################################################

# 	Start main routine
if __name__ == '__main__':
	AVG_NUM = int(input("Enter averaging period: "))
	readings = []
	i=0
	average=0
	
	#try:
	while(i<AVG_NUM):
		data = readline_blocking()
		if(is_number(data)):
			log_data(data)
			i+=1
			readings.append(int(data))
	# Calculate Average #
	#for num in readings:
	#	average+=num
	#average = average/AVG_NUM
	## Calculate Standard Deviation #
	#stdev = stdev(readings, average)
	[average, stdev] = stats(readings)
	print("Average: \t%s\nSt. Dev.:\t%s"%{average,stdev})
		
	#except:
	#	print("ERROR!  EXITING...")
	#finally:
	#	if (cur_path != str(os.getcwd())):
	#		os.chdir(cur_path)
	#	else:
	#		print("\nFailed to move back to original directory :(")
	#	if(ser.isOpen()):
	#		ser.close()
	#	sys.exit(0)			








