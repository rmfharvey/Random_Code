import serial, csv, sys, os, time, argparse	# Import full libraries
from math import sqrt 						# Import a single function from "math" library

#parser = argparse.ArgumentParser()		# Create object to accept extra command line arguments
#parser.add_argument('--port', dest='port', type=int)	# COM port
#parser.add_argument('-m', dest='monitor', type=bool)	# Monitoring mode
#parser.add_argument('-l', dest='logging', type=bool)	# Logging mode
#args = parser.parse_args()								# Put all argument values in a list

#sys.argv.append('-m') 		#add -m for .exe build

#### System Arguments ###################################################################
# To run script with no options, in the command line, type "python counter_stats.py"
# To run script with an option append the command line with the option, ex. "python counter_stats.py -m" to in monitoring mode 
class sysarg_t:
	def __init__(self):
		self.VERBOSE = False
		self.LOGGING = False
		self.MONITOR = False
		self.HELP = False
	def set_options(self):
		if "-h" in sys.argv:
			ARG.HELP = True
		if "-v" in sys.argv:
			ARG.VERBOSE = True
		if "-l" in sys.argv:
			ARG.LOGGING = True
			ARG.MONITOR = False
		if "-m" in sys.argv:
			ARG.MONITOR = True
			ARG.LOGGING = False
		
ARG = sysarg_t()
ARG.set_options()
#### System Arguments END ###############################################################

def enum_ports():		# Enumerate all COM ports and return the list
	ports = ['COM%s' % (i + 1) for i in range(256)]
	result = []
	for port in ports:
		try:	# Try to open a connection on some COM port, if no exception, close the connection and add the port to the list
			s = serial.Serial(port)
			s.close()
			result.append(port)
		except (OSError, serial.SerialException):
			pass
	return result	# Return the list of available ports

def is_number(st):	# Test if a string represents a number
	try:
		float(st)	# Cast string as a float
		return True	# If no exception, return true
	except ValueError:	# If the string wasn't a number, return false
		return False
	except:
		print("ERROR in function is_number()")
		sys.exit(0)		
	
def line_to_int(utf8_line):		# Convert a utf-8 string to an int
	value = 0
	try:
		for n in utf8_line:		# For each char in the utf-8 string, shift value, cast char as int and add
			if is_number(n):
				value = 10*value +int(n)
		return value
	except:
		print("line_to_int failed.\n")
		return -1
		
def stats(arr):		# Takes an array and returns the average value and standard deviation
	try:
		length = len(arr)
		average = 0
		for i in arr:
			average += i
		average /= length
		stdev = 0
		for j in arr:
			stdev += (j-average)**2
		stdev = sqrt(stdev/length)
		return (average, stdev)
	except:
		print("Stats failed.  Check the input array.\n")

	
#### Startup Text #############################################################
print("\nDorado Material Bay\n"
	  "Ultrasonics counter logging and stats\n"	
      "Python Version %s\n"
	  "Ross Harvey\n"
	  "10/23/2015\n\n"
	  "Run with arg -h (i.e. python %s -h) to see help menu.\n"%(sys.version, sys.argv[0]))
print("Available COM ports: %s\n"%enum_ports())
#### Startup Text END #########################################################

#### Serial Init ##############################################################
COM_PORT = int(input("Select COM port: "))	# Prompt user to enter the COM port
k22f = serial.Serial(port=(COM_PORT-1),		# Initialize the serial connection with given parameters
					 baudrate=115200,
					 timeout = 0.01)
print ("Connection started on %s\n"
		   "----------------------------------------------------------------------\n"%k22f.name)
#### Serial Init END ##########################################################

i = 0

if ARG.LOGGING:
	try:
		#### CSV ######################################################################
		file = open("us_count_stats.csv", 'w', newline='')
		try:
			outfile = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			outfile.writerow(["Counter","Count Value","Read Time"])
		except:
			print("csv file creation failed. Exiting...")
			sys.exit(0)
		#### CSV END ##################################################################
	
		READMAX = 10000		# number of readings to take
		readings_arr = [[0 for x in range(0,2)] for x in range(0,READMAX)]	# Initialize 2D array to hold read values and the elapsed time between reads 
		read_num = 0
		
		flushed = False
		while not flushed:	# Discard one reading to avoid a misaligned first read
			try:
				k22f.readline().decode('utf-8')
				flushed = True
			except:
				pass
		while read_num < READMAX:
			read_success = False	# utf-8 encoding sometimes fails so exception handling is included to let script execute fully
			temp_read = 0
			t1 = 0
			t0 = time.clock()	# Read system clock at start
			while not read_success:
				try:
					temp_read = line_to_int(k22f.readline().decode('utf-8'))	# Read a '\n' terminated line and decode as 'utf-8'
					t1 = time.clock()
					read_success = True
				except:
					pass
			if temp_read<1000:
				readings_arr[read_num] = [temp_read,(t1-t0)*1000000]	# Append values to array
				read_num += 1
		count=0
		
		count_stats = stats(readings_arr[0])	# Return stats for counter values
		time_stats = stats(readings_arr[1])		# Return stats for elapsed time values
	
		print()
		print("Stats:\nRead Time Avg:\t\t%3.2d us\n"
			"Count Avg:\t\t%3.0d LSBs\n"
			"\n"
			"Read Time Std Dev:\t%d us\n"
			"Count Std Dev:\t\t%d"%(time_stats[0],count_stats[0],time_stats[1],count_stats[1]))
		file.close()	# Close CSV
		k22f.close()	# Close serial connection
		sys.exit(0)	
	except:
		pass
	finally:		# If an exception is raised at runtime, close file and serial connection before exiting
		file.close()
		k22f.close()
		sys.exit(0)

elif ARG.MONITOR:	# Print stats to terminal until user ends the script
	try:
		i=0
		while True:
			val = line_to_int(k22f.readline().decode('utf-8'))
			if i==1000:
				print("Count: %s   "%val, end='\r')
				i=0
			else:
				i+=1
	except:
		sys.exit(0)
	
	
	
	
	
	
	
	
	
	