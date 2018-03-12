/*
 * FPGA Interface C API Example for C/C++ Development Tools for NI Linux Real-Time, Eclipse Edition
 *
 * NOTE: In order to run this example, you must:
 * 1) Configure your Eclipse environment and install drivers as specified in this white paper: http://www.ni.com/white-paper/14625/en
 * 2) Install software on your NI Real-Time Linux target.
 * 3) Connect to your NI Real-Time Linux target as specified in the above white paper.
 * 4) Transfer your NiFpga_FPGA.lvbitx file to the your Linux RT system in the same directory as your built code.
 *
 * The bit file this example uses is for the cRIO-9068. To use a different target you must rebuild the FPGA bit file using LabVIEW FPGA
 * and then use the FPGA Interface C API to regenerate the NiFpga_FPGA.h file. For instructions on using the FPGA Interface C API, refer
 * to the Examples topic of the FPGA Interface C API Help, located under
 * Start>>All Programs>>National Instruments>>FPGA Interface C API
 *
 * For an FPGA Interface C API tutorial, see: http://www.ni.com/white-paper/8638/en
 */

/* Includes all FPGA Interface C API functions required */
#include "NiFpga_FPGA.h"
/* Required for console interactions */
#include <stdio.h>
/* Required for sleep() */
#include <unistd.h>

/* Define functions */
int GetUserInputNumber();
void ChassisTemperature(NiFpga_Session, NiFpga_Status*);
void LedSequence(NiFpga_Session, NiFpga_Status*);
int FourElementAverage(NiFpga_Session, NiFpga_Status*);
void WhiteGaussianNoise(NiFpga_Session, NiFpga_Status*, NiFpga_IrqContext*);

int main()
{
	int UserInput;
	bool Stop = false;
	NiFpga_Session session;
	NiFpga_IrqContext irqContext;

	/* Initialize must be called first. Store error information in "status" */
	printf("Initializing...\n");
	NiFpga_Status status = NiFpga_Initialize();

	/* opens a session with the FPGA, downloads the bitstream, and runs the FPGA, storing any error info in "status" */
	printf("Opening a Session...\n");
	NiFpga_MergeStatus(&status, NiFpga_Open(NiFpga_FPGA_Bitfile,
											NiFpga_FPGA_Signature,
											"RIO0",
											0,
											&session));

	/* reserve a context for this thread to wait on IRQs */
	NiFpga_MergeStatus(&status, NiFpga_ReserveIrqContext(session, &irqContext));

	/* Enter main loop. Exit if there is an error or the user requests the program to end */
	while (NiFpga_IsNotError(status) && !Stop)
	{
		/* Generate Menu */
		printf("\n");
		printf("|---------------------------------------------------------------|\n");
		printf("| Enter 0 to Exit Program                                       |\n");
		printf("| Enter 1 to Execute LED Sequence                               |\n");
		printf("| Enter 2 to Read the Chassis Temperature                       |\n");
		printf("| Enter 3 to Compute a 4-element Integer Average                |\n");
		printf("| Enter 4 to Read White Gaussian Noise from a DMA FIFO          |\n");
		printf("|---------------------------------------------------------------|\n");

		UserInput = GetUserInputNumber();

		printf("You entered: %d\n\n", UserInput);

		switch(UserInput)
		{
		case 0:
			printf("Initiating Shutdown Procedure\n");
			Stop = true;
			break;
		case 1:
			LedSequence(session, &status);
			break;
		case 2:
			ChassisTemperature(session, &status);
			break;
		case 3:
			FourElementAverage(session, &status);
			break;
		case 4:
			WhiteGaussianNoise(session, &status, &irqContext);
			break;
		default:
			printf("INVALID INPUT! Please choose an integer between 0 and 4.\n");
		}

	}

	/* unreserve IRQ status to prevent memory leaks */
	NiFpga_MergeStatus(&status, NiFpga_UnreserveIrqContext(session, irqContext));

	/* Close the session */
	NiFpga_MergeStatus(&status, NiFpga_Close(session, 0));

	/* Finalize must be called before exiting program and after closing FPGA session */
	NiFpga_MergeStatus(&status, NiFpga_Finalize());

	/* Return an error code if there is an error */
	if(NiFpga_IsError(status))
	{
		printf("Error! Exiting program. LabVIEW error code: %d\n", status);
	}
	return 0;
}

/*
 * Function to get an input integer from the stream.
 * Returns the number entered. Returns -1 for invalid input
 * A number followed by a string of non-numerics will get interpreted as that number
 * For example, "32reqwd" will return "32".
 * This function also prints out a warning message for each extra character entered into the stream
 *
 * @return Number
 */
int GetUserInputNumber()
{
	int input;
	int Number = -1;

	/* Get number from stream */
	scanf("%d", &Number);

	/* Clear out extra characters from stream. Set limit at 100 characters to prevent infinite loops */
	int i=0;
	while(i<100)
	{
		input = getchar();
		//exit this loop if we hit EOF (-1) or a new line character
		if (input == '\n' || input == -1) break;
		printf("WARNING: Extra character(s) detected! Clearing stream: %d\n",input);
		i++;
	}
	return Number;

}

/*
 * Function sends 4 integers down to the FPGA to calculate a 4-element average.
 * Each number is entered by the user one at a time.
 * This function utilizes a Host-to-Target DMA FIFO as well as a basic IO Read.
 *
 * /// Note: Using a DMA for only four elements is not efficient. This is a
 * /// simple example function showing how to use a Host-to-Target DMA FIFO
 *
 * @param[in]		session		Uses FPGA session reference
 * @param[in,out]	status		Uses and updates error status
 * @return 			Average
 */
int FourElementAverage(NiFpga_Session session, NiFpga_Status *status)
{
	int average = 0;
	unsigned int i = 0;
	unsigned int NumberToAverage = 4;
	int FifoData[4] = {0,0,0,0};
	size_t FifoEmptyElements;

	printf("We will prompt you to enter one element at a time.\n");
	printf("We will then FIFO the data to the FPGA for computation.\n");
	printf("The average will be rounded to the nearest integer.\n");
	/* Get the numbers to average */
	for(i=0; i<NumberToAverage; i++)
	{
		printf("Number %d: ",i+1);
		FifoData[i] = GetUserInputNumber();
	}
	printf("\nComputing the Average of these numbers:\n");
	for(i=0; i<NumberToAverage; i++)
	{
		printf("%d, ",FifoData[i]);
	}
	printf("\n\n");

	/* FIFO the data to the FPGA for computation */
	NiFpga_MergeStatus(status, NiFpga_WriteFifoI32(session,
													NiFpga_FPGA_HostToTargetFifoI32_ElementsToAverage,
													FifoData,
													NumberToAverage,
													1000,
													&FifoEmptyElements));
	/* Read FPGA indicator to see average */
	NiFpga_MergeStatus(status, NiFpga_ReadI32(session,
												NiFpga_FPGA_IndicatorI32_4ElementAverage,
												&average));
	/* If there is an error, do not print an incorrect result. Calling function will handle error */
	if (!NiFpga_IsError(*status))
	{
		//Print result
		printf("Calculated Integer Average: %d\n",average);
	}

	return average;
}

/*
 * Functions interfaces with the FPGA to read the current chassis temperature through a read/write control.
 * This function utilizes basic FPGA IO Reads
 *
 * @param[in]		session		Uses FPGA session reference
 * @param[in,out]	status		Uses and updates error status
*/
void ChassisTemperature(NiFpga_Session session, NiFpga_Status *status)
{
	float Temperature = 0;
	int16_t RawTemperature = 0;

	printf("Acquiring Chassis Temperature...\n");

	NiFpga_MergeStatus(status, NiFpga_ReadI16(session,
											 NiFpga_FPGA_IndicatorI16_ChassisTemperature,
											 &RawTemperature));
	//To convert temperature returned from the FPGA to Celsius, divide by 4
	Temperature = RawTemperature;
	Temperature /= 4;
	printf("Measured Internal Chassis Temperature is %.1f Celsius\n",Temperature);
}

/*
 * This function launches a simple LED sequence. It is easy to change the sequence
 * By default the sequence is "Green --> Orange --> Off" with a one-second pause between each LED status change
 * This function utilizes basic FPGA IO Writes
 *
 * @param[in]		session		Uses FPGA session reference
 * @param[in,out]	status		Uses and updates error status
 */
void LedSequence(NiFpga_Session session, NiFpga_Status *status)
{
	int LED_SequenceLength = 3;
	int i;

	printf("Launching LED Sequence...\n");
	for(i=0; i < LED_SequenceLength; i++)
	{
		/* Write to an FPGA control to set the LED to be green */
		NiFpga_MergeStatus(status, NiFpga_WriteU8(session,
													NiFpga_FPGA_ControlU8_UserFpgaLed,
													1));
		sleep(1);
		/* Set the LED to be orange */
		NiFpga_MergeStatus(status, NiFpga_WriteU8(session,
													NiFpga_FPGA_ControlU8_UserFpgaLed,
													2));
		sleep(1);
		/* Turn the LED off */
		NiFpga_MergeStatus(status, NiFpga_WriteU8(session,
													NiFpga_FPGA_ControlU8_UserFpgaLed,
													0));
		sleep(1);
		printf("LED Sequence %d of %d Completed\n",i+1,LED_SequenceLength);
	}
}

/*
 * This function acquires White Gaussian Noise with RMS of 1 using the FPGA to generate the noise
 * It prints all values acquired to the stream. The FPGA returns an I16, so this function scales the number
 * This function relies on interrupts to synchronize the FPGA to host DMA transfer
 * Utilizes IRQ synchronization and an FPGA to Host DMA FIFO
 *
 * @param[in]		session		Uses FPGA session reference
 * @param[in,out]	status		Uses and updates error status
 * @param[in]		irqContext	Uses irqContext for IRQ
 */
void WhiteGaussianNoise(NiFpga_Session session, NiFpga_Status *status, NiFpga_IrqContext *irqContext)
{
	/* DMA FIFO related variables */
	unsigned int Number_Acquire = 40;
	int16_t Fifo_Data[Number_Acquire];
	unsigned int Elements_Remaining;
    unsigned int Fifo_Timeout = Number_Acquire*10;

    /* IRQ related variables */
	uint32_t irqsAsserted;
    uint32_t irqTimeout = 1000; //1 second
    NiFpga_Bool TimedOut = false;

    double WhiteNoise;
	unsigned int i = 0;

	printf("Acquiring White Gaussian Noise Using a DMA FIFO...\n");

	//Wait on IRQ to ensure FPGA is ready
	NiFpga_MergeStatus(status, NiFpga_WaitOnIrqs(session,
												 irqContext,
												 NiFpga_Irq_0,
												 irqTimeout,
												 &irqsAsserted,
												 &TimedOut));

    /* if an IRQ was asserted */
    if (NiFpga_IsNotError(*status) && !TimedOut)
    {
		// configure number of random elements to acquire
		NiFpga_MergeStatus(status, NiFpga_WriteU32(session,
													NiFpga_FPGA_ControlU32_WhiteNoiseDataLength,
													Number_Acquire));
		// Acknowledge IRQ to begin DMA acquisition
		NiFpga_MergeStatus(status, NiFpga_AcknowledgeIrqs(session,
														  irqsAsserted));

		//Read FIFO data into the Fifo_Data array
		NiFpga_MergeStatus(status, NiFpga_ReadFifoI16(session,
														NiFpga_FPGA_TargetToHostFifoI16_WhiteGaussianNoise,
														Fifo_Data,
														Number_Acquire,
														Fifo_Timeout,
														&Elements_Remaining));

		//Check for error before printing data
		if(!NiFpga_IsError(*status))
		{
			printf("Successfully Generated %d random numbers:\n",Number_Acquire);
			//Print out data
			for(i=0; i<Number_Acquire; i++)
			{
				//Normalize FPGA data. FPGA is I16 with RMS of 6000, max possible value limited by I16 (>5x RMS)
				WhiteNoise = Fifo_Data[i];
				WhiteNoise /= 6000;
				printf("%.2f\n",WhiteNoise);
			}
		}
    }
    if(TimedOut){
    	printf("IRQ Timed out! Please examine FPGA code.\n");
    }
}
