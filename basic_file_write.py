from nifpga import Session
import time

bitfilepath = "mybitfile.lvbitx"
targetname = "RIO0"

indicators = [] #Initialize an empty list of indicators to reference

log_file = open("log.txt", "w")

num_data_points = 10000 #Set the number of data points to log for

#with Session(bitfile = bitfilepath, resource = targetname) as session:
	#session.reset() #Stop FPGA logic and puts it into the default state
	
	#session.run() #Run FPGA logic
	
	#Data acquisition here
t1 = time.time()
for i in range(num_data_points):
	#	my_indicator = session.registers['My Indicator']
	my_indicator = i
	#Log data here
	log_file.write("{0:.4f}\n".format(my_indicator))
	print(my_indicator)
	
print(time.time() - t1)