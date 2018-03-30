from nifpga import Session

with Session(bitfile="MyBitfile.lvbitx", resource="RIO0") as session:
    # Reset stops the logic on the FPGA and puts it in the default state.
    # May substitute reset with download if your bitfile doesn't support it.
    session.reset()

    # Add Initialization code here!
    # Write initial values to controls while the FPGA logic is stopped.

    # Start the logic on the FPGA
    session.run()

    # Add code that interacts with the FPGA while it is running here!