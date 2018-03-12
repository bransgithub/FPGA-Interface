FPGA Interface C API Example for C/C++ Development Tools for NI Linux Real-Time, Eclipse Edition

Contains C Code as well as LabVIEW code. The LabVIEW code contains a basic LabVIEW Real-Time test VI, which is not needed for this example.

NOTE: In order to run this example, you must:
1) Configure your Eclipse environment and install drivers as specified in this white paper: http://www.ni.com/white-paper/14625/en
2) Install software on your NI Real-Time Linux target.
3) Connect to your NI Real-Time Linux target as specified in the above white paper.
4) Transfer your NiFpga_FPGA.lvbitx file to the your Linux RT system in the same directory as your built code.

The bit file this example uses is for the cRIO-9068. To use a different target you must rebuild the FPGA bit file using LabVIEW FPGA and then use the FPGA Interface C API to regenerate the NiFpga_FPGA.h file. For instructions on using the FPGA Interface C API, refer to the Examples topic of the FPGA Interface C API Help, located under Start>>All Programs>>National Instruments>>FPGA Interface C API

For an FPGA Interface C API tutorial, see: http://www.ni.com/white-paper/8638/en
