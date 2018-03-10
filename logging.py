from nifpga import Session

bitfilepath = "mybitfile.lvbitx"
targetname = "RIO0"

#indicators = [] #Initialize an empty list of indicators to reference

log_file = open("log.txt", "w")

num_data_points = 10000 #Set the number of data points to log for

with Session(bitfile = bitfilepath, resource = targetname) as session:
	session.reset() #Stop FPGA logic and puts it into the default state
	
	session.run() #Run FPGA logic
	
	#Data acquisition here
	
	for i in range(num_data_points):
		my_indicator = session.registers['My Indicator']
		
		#Log data here		
		log_file.write("{0:.4f}\n".format(my_indicator))
		#print(my_indicator)