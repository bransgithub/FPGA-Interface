from nifpga import Session

bitfilepath = "mybitfile.lvbitx"
targetname = "RIO0"

indicators = [] #Initialize an empty list of indicators to reference

with Session(bitfile = bitfilepath, resource = targetname) as session:
	session.reset() #Stop FPGA logic and puts it into the default state
	
	session.run() #Run FPGA logic
	
	#Data acquisition here
	
	#Log data here