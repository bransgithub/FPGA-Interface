from nifpga import Session

bitfilepath = "MyBitfile.lvbitx"
targetname = "10.1.128.157/RIO0"

with Session(bitfile = bitfilepath, resource = targetname) as session:
	# Reset stops the logic on the FPGA and puts it in the default state.
	# May substitute reset with download if your bitfile doesn't support it.
	session.reset()

	# Add Initialization code here!
	# Write initial values to controls while the FPGA logic is stopped.

	# Start the logic on the FPGA
	session.run()
	
	Noise_length = session.registers['White Noise Data Length']
	
	Noise_length.write(10)
	
	White_Gaussian_FIFO = session.fifos['White Gaussian Noise']
	White_Gaussian_FIFO.start() #Start the FIFO

	Fifo_Data = White_Gaussian_FIFO.read(10, timeout_ms = 500)
	
	#Normalize (Divide by 6000, since that is the RMS) and Print data	
	print(Fifo_Data.data / 6000)
 