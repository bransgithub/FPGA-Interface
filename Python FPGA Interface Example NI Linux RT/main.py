#Example for Python FPGA Interface ft. the following functions:
#Chassis Temperature
#LED Sequences
#Number Averaging
#White Gaussian Noise

from nifpga import Session
import time

bitfilepath = "MyBitfile.lvbitx"
targetname = "RIO0"

num_data_points = 10000 #Set the number of data points to log for
		
def ChassisTemperature():

	with Session(bitfile = bitfilepath, resource = targetname) as session:
		session.reset() #Stop FPGA logic; put into default state
		session.run() #Run FPGA logic
		temp_indicator = session.registers['Chassis Temperature']
		temperature = temp_indicator.read() / 4 #Divide temperature by 4 to convert FPGA -> Celsius
		print("The Internal Chassis Temperature is {0:.1f} C".format(temperature))

def LedSequence():

	with Session(bitfile = bitfilepath, resource = targetname) as session:
		session.reset() #Stop FPGA logic; put into default state
		session.run() #Run FPGA logic
		LED_control = session.registers['User Fpga Led']
		for i in range(3):
			LED_control.write(1) #green
			time.sleep(1) #1 second wait
			LED_control.write(2) #orange
			time.sleep(1)
			LED_control.write(0)
			print("LED Sequence {0} of 3 Completed".format(i + 1)) 
		
def FourElementAverage():
	
	FifoData = []
	
	print("Enter one integer element at a time.\n")
	print("Data will be sent to the FPGA via FIFO, and the rounded integer average will be returned.\n")
	
	i = 0
	
	#Loop to accept integer inputs
	while i < 4:
		try:
			FifoData.append( int( input("Enter a number: ".format(i + 1)) ) )
			i += 1
		except: #Repeat loop iteration if invalid entry
			print("Invalid input. Please enter an integer. ")
			pass
			
	print("Computing the average of {0}, {1}, {2}, and {3}...".format(FifoData[0], FifoData[1], FifoData[2], FifoData[3]))

	with Session(bitfile = bitfilepath, resource = targetname) as session:
		session.reset() #Stop FPGA logic; put into default state
		session.run() #Run FPGA logic
		
		Average = session.registers['4-Element Average'] #Indicator for the average value
		
		Host_Target_FIFO = session.fifos['Elements To Average'] #Obtain the host to target FIFO
		Host_Target_FIFO.start() #Start the FIFO
		
		for j in range(4):
			Host_Target_FIFO.write(FifoData[j], timeout_ms = 100) #Writes numeric data to the FIFO, 100 ms timeout
		
		data = Average.read()
		
		print("The integer average is {0:.2f}".format(data)) 
		
def WhiteGaussianNoise():

	#Generate log file. This will replace an existing file of the same name.
	log_file = open("log.txt", "w")
	
	#DMA FIFO Variables:
	Number_Acquire = 40
	Fifo_Timeout = Number_Acquire*10
	
	#IRQ Variables:
	irqTimeout = 1000
	irq = 0 #IRQ 0 is the default IRQ if unwired
	
	with Session(bitfile = bitfilepath, resource = targetname) as session:
		session.reset() #Stop FPGA logic; put into default state
		session.run() #Run FPGA logic
		
		Noise_length = session.registers['White Noise Data Length'] #Assign control to set # of White noise data points
		
		White_Gaussian_FIFO = session.fifos['White Gaussian Noise'] #Assign Target to Host FIFO
		White_Gaussian_FIFO.start() #Start the FIFO
		
		#Wait on IRQ to find if FPGA is ready
		irq_status = session.wait_on_irqs(irq, irqTimeout) 
		
		if irq_status.timed_out == True:
			print("Timed out while waiting for interrupt.")
		
		#If IRQ asserted:		
		if irq in irq_status.irqs_asserted:
			print("IRQ 0 was asserted.")
			
			Noise_length.write(Number_Acquire)
			
			#Acknowledge IRQ
			session.acknowledge_irqs(irq_status.irqs_asserted)
			
			#Read FIFO data into Fifo_Data array
			Fifo_Data = White_Gaussian_FIFO.read(Number_Acquire, timeout_ms = Fifo_Timeout)
			
			#Normalize, log and print data	
			for i in range(0, Number_Acquire):
				RMS_val = int (Fifo_Data.data[i]) / 6000.0 #Divide by 6000, since that is the RMS
				log_file.write("{0:.2f}\n".format(RMS_val)) #Add data point to the log file
				print(RMS_val)
		else:
			print("IRQ 0 was not asserted.")
			
	log_file.close()
		
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
		user_input = 5 #If not a value from 0-4, set to an invalid number

	if user_input == 0:
		print("Shutting Down the Program.")
		Stop = True
	elif user_input == 1:
		print("Executing LED Sequence...")
		LedSequence()
	elif user_input == 2:
		print("Reading Chassis Temperature...")
		ChassisTemperature()
	elif user_input == 3:
		print("Computing a 4-element Integer Average...")
		FourElementAverage()
	elif user_input == 4:
		print("Reading 40 Elements of White Gaussian Noise...")
		WhiteGaussianNoise()
	else:
		print("Invalid Input. Please Enter an Integer Between 0 and 4.")

	













