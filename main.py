from nifpga import Session

bitfilepath = "mybitfile.lvbitx"
targetname = "RIO0"

log_file = open("log.txt", "w")

num_data_points = 10000 #Set the number of data points to log for

# with Session(bitfile = bitfilepath, resource = targetname) as session:
	# session.reset() #Stop FPGA logic and puts it into the default state
	
	# session.run() #Run FPGA logic
	
	#Data acquisition here
	
	# for i in range(num_data_points):
		# my_indicator = session.registers['My Indicator']
		
		#Log data here		
		# log_file.write("{0:.4f}\n".format(my_indicator))
		#print(my_indicator)

	# with Session(bitfile = bitfilepath, resource = targetname) as session:
		# session.reset() #Stop FPGA logic; put into default state
		# session.run() #Run FPGA logic
		
def ChassisTemperature():
	with Session(bitfile = bitfilepath, resource = targetname) as session:
		session.reset() #Stop FPGA logic; put into default state
		session.run() #Run FPGA logic
		#**** add temperature indicator name below
		temp_indicator = session.registers['Temp Ind']
		temperature = temp_indicator.read() / 4 #Divide temperature by 4 to convert FPGA -> Celsius
		print("The Internal Chassis Temperature is {0:.1f}".format(temperature))

# def LedSequence():

# def FourElementAverage():

# def WhiteGaussianNoise():

print("\n|-------------- Python FPGA Interface Example ------------------|")
print("| Enter 0 to Exit Program                                       |")
print("| Enter 1 to Execute LED Sequence                               |")
print("| Enter 2 to Read the Chassis Temperature                       |")
print("| Enter 3 to Compute a 4-element Integer Average                |")
print("| Enter 4 to Read White Gaussian Noise from a DMA FIFO          |")
print("|---------------------------------------------------------------|\n")

Stop = False

while Stop == False:

	try:
		user_input = int( input("Enter a number: ") ) #Accept user input from 0-4
	except:
		user_input = 5

	if user_input == 0:
		print("Shutting Down the Program.")
		Stop = True
	elif user_input == 1:
		print("Executing LED Sequence...")
	elif user_input == 2:
		print("Reading Chassis Temperature...")
	elif user_input == 3:
		print("Computing a 4-element Integer Average...")
	elif user_input == 4:
		print("Reading White Gaussian Noise...")
	else:
		print("Invalid Input. Please Enter an Integer Between 0 and 4.")

	













