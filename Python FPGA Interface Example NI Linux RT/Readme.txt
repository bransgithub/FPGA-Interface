-NI FPGA Interface Python Example-

This example was based entirely off the C FPGA Interface Example for NI Linux RT by ColdenR:
https://forums.ni.com/t5/NI-Linux-Real-Time-Documents/FPGA-Interface-C-API-Example-for-NI-Linux-Real-Time-and-Eclipse/ta-p/3512138

Follow the FPGA Interface Python documentation for Getting Started materials:
http://nifpga-python.readthedocs.io/en/latest/index.html

The Python script interfaces with a pre-compiled bitfile for the CompactRIO-9068. If you have a 9068, you can use the bitfile provided in this example.
The script can be run directly on the Real-Time processor of the cRIO, as it is NI Linux RT. 

You can use WebDav to place the Python script and the bitfile onto your cRIO-9068:
"Using WebDAV to Transfer Files to Real-Time Target": https://knowledge.ni.com/KnowledgeArticleDetails?id=kA00Z0000019PlESAU

There are 4 different functions that showcase the functionality of the Python FPGA Interface:

ChassisTemperature(): Use indicators to display the chassis temperature
LedSequence(): Use controls to change User LEDs on the cRIO-9068
FourElementAverage(): Use a Host to Target FIFO to calculate a 4-element average on the FPGA and display it
WhiteGaussianNoise(): Acknowledge an interrupt on the FPGA, and read generated noise data from a Target to Host FIFO


