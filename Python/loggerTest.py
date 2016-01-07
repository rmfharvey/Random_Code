import serial
import csv
import sys
import glob


#def enum_ports():
#	ports = ['COM%s' % (i + 1) for i in range(256)]
#
#	result = []
#	for port in ports:
#		try:
#			s = serial.Serial(port)
#			s.close()
#			result.append(port)
#		except (OSError, serial.SerialException):
#			pass
#	return result

print("HERE")

#### COM Setup #########################################################################
COMPORT = 22	
BAUDRATE = 256000
#COM_PORT = int(input("Enter COM port Number: "))
#print("\n\r\n\r")
#print("Available ports:")
#print(enum_ports())
#print("\n\n\r")

print("HERE")
#try:
k22f = serial.Serial(port=(COMPORT-1),baudrate=BAUDRATE,timeout = 0.01)
print ("Connection started on %s\n at %s kbps"
		   "----------------------------------------------------------------------\n"%(k22f.name, BAUDRATE/1000))
#except:
#	print("CONNECTION FAILED.  EXITING...")
#	sys.exit(0)
### COM Setup END #####################################################################

#Packet
# C-interp 	uint16_t voltage, uint16_t current, char range, "\n"
# Py-Interp	char, char, char, char, char, '\n'
print("HERE")
TXSIZE = 200
resultsArray = []
k22f.readline()
for i in range(0,TXSIZE):
	print("HERE")
	resultsArray.append(list(k22f.readline()))	# Read lines until transmit period is over

with open("loggingFile.csv", 'a', newline='') as file:
	print("HERE")
	for j in resultsArray:
		output = csv.writer(file)
		output.writerow([ ord(j[0])<<8+ord(j[1]) , ord(j[2])<<8+ord(j[3]) , j[4] ])
		file.close()