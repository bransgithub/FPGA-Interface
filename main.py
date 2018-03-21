#Example for Python FPGA Interface ft. the following functions:
#Chassis Temperature
#LED Sequences
#Number Averaging
#White Gaussian Noise

from nifpga import Session
import time

bitfilepath = "mybitfile.lvbitx"
targetname = "RIO0"

log_file = open("log.txt", "w")

num_data_points = 10000 #Set the number of data points to log for
		
def ChassisTemperature():

	with Session(bitfile = bitfilepath, resource = targetname) as session:
		session.reset() #Stop FPGA logic; put into default state
		session.run() #Run FPGA logic
		#**** add temperature indicator name below
		temp_indicator = session.registers['Chassis Temperature']
		temperature = temp_indicator.read() / 4 #Divide temperature by 4 to convert FPGA -> Celsius
		print("The Internal Chassis Temperature is {0:.1f}".format(temperature))

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
	
	print("Enter one element at a time.")
	print("Data will be sent to the FPGA via FIFO, and the rounded integer average will be returned")
	
	for i in range(4):
		FifoData[i] = int( input("Enter number {0}".format(i + 1)) )
		
	print("Computing the average of {0}, {1}, {2}, and {3}...".format(FifoData[0], FifoData[1], FifoData[2], FifoData[3]))

	with Session(bitfile = bitfilepath, resource = targetname) as session:
		session.reset() #Stop FPGA logic; put into default state
		session.run() #Run FPGA logic
		
		Average = session.registers('4-Element Average') #Indicator for the average value
		
		Host_Target_FIFO = session.registers('Elements To Average') #Obtain the host to target FIFO
		Host_Target_FIFO.start() #Start the FIFO
		
		for i in range(4):
			Host_Target_FIFO.write(FifoData[i], timeout_ms = 100) #Writes numeric data to the FIFO, 100 ms timeout
		
		print("The average is {0.2f}".format(Average)) 
		
def WhiteGaussianNoise():

	#DMA FIFO Variables:
	Number_Acquire = 40
	Fifo_Timeout = Number_Acquire*10
	
	#IRQ Variables:
	irqTimeout = 1000
	irq = 0 #IRQ 0 is the default IRQ if unwired
	
	with Session(bitfile = bitfilepath, resource = targetname) as session:
		session.reset() #Stop FPGA logic; put into default state
		session.run() #Run FPGA logic
		
		White_Gaussian_FIFO = session.registers('White Gaussian Noise')
		White_Gaussian_FIFO.start() #Start the FIFO
		
		#Wait on IRQ to find if FPGA is ready
		irq_status = session.wait_on_irqs(irq, irqTimeout) 
		
		if irq_status.timed_out = True:
			print("Timed out while waiting for interrupt.")
		
		#If IRQ asserted:		
		if irq in irq_status.irqs_asserted:
			print("IRQ 0 was asserted.")
					
			#Acknowledge IRQ
			session.acknowledge_irqs(irq_status.irqs_asserted)
			
			#Read FIFO data into Fifo_Data array
			Fifo_Data = White_Gaussian_FIFO.read(Number_Acquire, timeout_ms = Fifo_Timeout)
			
			#Normalize (Divide by 6000, since that is the RMS) and Print data	
			print(Fifo_Data.data / 6000)
			
		else:
			print("IRQ 0 was not asserted.")
		
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
	elif user_input == 2:
		print("Reading Chassis Temperature...")
	elif user_input == 3:
		print("Computing a 4-element Integer Average...")
	elif user_input == 4:
		print("Reading White Gaussian Noise...")
	else:
		print("Invalid Input. Please Enter an Integer Between 0 and 4.")

	













