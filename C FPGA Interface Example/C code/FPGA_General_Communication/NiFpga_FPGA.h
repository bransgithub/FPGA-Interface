/*
 * Generated with the FPGA Interface C API Generator 13.0.0
 * for NI-RIO 13.0.0 or later.
 */

#ifndef __NiFpga_FPGA_h__
#define __NiFpga_FPGA_h__

#ifndef NiFpga_Version
   #define NiFpga_Version 1300
#endif

#include "NiFpga.h"

/**
 * The filename of the FPGA bitfile.
 *
 * This is a #define to allow for string literal concatenation. For example:
 *
 *    static const char* const Bitfile = "C:\\" NiFpga_FPGA_Bitfile;
 */
#define NiFpga_FPGA_Bitfile "NiFpga_FPGA.lvbitx"

/**
 * The signature of the FPGA bitfile.
 */
static const char* const NiFpga_FPGA_Signature = "7D9055FC1762820C526BEC0E19C32119";

typedef enum
{
   NiFpga_FPGA_IndicatorBool_WhiteNoiseDataTimeout = 0x18002,
} NiFpga_FPGA_IndicatorBool;

typedef enum
{
   NiFpga_FPGA_IndicatorI16_ChassisTemperature = 0x1800A,
} NiFpga_FPGA_IndicatorI16;

typedef enum
{
   NiFpga_FPGA_IndicatorI32_4ElementAverage = 0x1800C,
} NiFpga_FPGA_IndicatorI32;

typedef enum
{
   NiFpga_FPGA_ControlU8_UserFpgaLed = 0x18012,
} NiFpga_FPGA_ControlU8;

typedef enum
{
   NiFpga_FPGA_ControlU32_WhiteNoiseDataLength = 0x18004,
} NiFpga_FPGA_ControlU32;

typedef enum
{
   NiFpga_FPGA_TargetToHostFifoI16_WhiteGaussianNoise = 0,
} NiFpga_FPGA_TargetToHostFifoI16;

typedef enum
{
   NiFpga_FPGA_HostToTargetFifoI32_ElementsToAverage = 1,
} NiFpga_FPGA_HostToTargetFifoI32;

#endif
