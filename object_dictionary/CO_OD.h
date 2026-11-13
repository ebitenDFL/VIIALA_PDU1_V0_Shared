/*
 * Copyright (c) 2019 Vestas Wind Systems A/S
 *
 * SPDX-License-Identifier: Apache-2.0
 */

/*******************************************************************************

   File - CO_OD.c/CO_OD.h
   CANopen Object Dictionary.

   This file was automatically generated with libedssharp Object
   Dictionary Editor v0.8-7-g2e53bbc   DON'T EDIT THIS FILE MANUALLY !!!!
*******************************************************************************/


#ifndef CO_OD_H_
#define CO_OD_H_

/*******************************************************************************
   CANopen DATA TYPES
*******************************************************************************/
typedef bool_t BOOLEAN;
typedef uint8_t UNSIGNED8;
typedef uint16_t UNSIGNED16;
typedef uint32_t UNSIGNED32;
typedef uint64_t UNSIGNED64;
typedef int8_t INTEGER8;
typedef int16_t INTEGER16;
typedef int32_t INTEGER32;
typedef int64_t INTEGER64;
typedef float32_t REAL32;
typedef float64_t REAL64;
typedef char_t VISIBLE_STRING;
typedef oChar_t OCTET_STRING;

   #ifdef DOMAIN
   #undef DOMAIN
   #endif

typedef domain_t DOMAIN;

#ifndef timeOfDay_t
typedef union {
	unsigned long long ullValue;
	struct {
		unsigned long ms : 28;
		unsigned reserved : 4;
		unsigned days : 16;
		unsigned reserved2 : 16;
	};
} timeOfDay_t;
#endif

typedef timeOfDay_t TIME_OF_DAY;
typedef timeOfDay_t TIME_DIFFERENCE;


/*******************************************************************************
   FILE INFO:
      FileName:     objdict.eds
      FileVersion:  1
      CreationTime: 2:52PM
      CreationDate: 09-18-2019
      CreatedBy:
 ******************************************************************************/


/*******************************************************************************
   DEVICE INFO:
      VendorName:
      VendorNumber    0
      ProductName:    VIIALA_PDU1_V0
      ProductNumber:  0
 ******************************************************************************/


/*******************************************************************************
   FEATURES
*******************************************************************************/
  #define CO_NO_SYNC                     1      /* Associated objects: 1005-1007 */
  #define CO_NO_EMERGENCY                1      /* Associated objects: 1014, 1015 */
  #define CO_NO_TIME                     1      /* Associated objects: 1012, 1013 */
  #define CO_NO_SDO_SERVER               1      /* Associated objects: 1200-127F */
  #define CO_NO_SDO_CLIENT               0      /* Associated objects: 1280-12FF */
  #define CO_NO_LSS_SERVER               0      /* LSS Slave */
  #define CO_NO_LSS_CLIENT               0      /* LSS Master */
  #define CO_NO_RPDO                     4      /* Associated objects: 14xx, 16xx */
  #define CO_NO_TPDO                     5      /* Associated objects: 18xx, 1Axx */
  #define CO_NO_NMT_MASTER               0


/*******************************************************************************
   OBJECT DICTIONARY
*******************************************************************************/
   #define CO_OD_NoOfElements             77


/*******************************************************************************
   TYPE DEFINITIONS FOR RECORDS
*******************************************************************************/
/*1018    */ typedef struct {
	UNSIGNED8 maxSubIndex;
	UNSIGNED32 vendorID;
	UNSIGNED32 productCode;
	UNSIGNED32 revisionNumber;
	UNSIGNED32 serialNumber;
}              OD_identity_t;
/*1200    */ typedef struct {
	UNSIGNED8 maxSubIndex;
	UNSIGNED32 COB_IDClientToServer;
	UNSIGNED32 COB_IDServerToClient;
}              OD_SDOServerParameter_t;
/*1280    */ typedef struct {
	UNSIGNED8 maxSubIndex;
	UNSIGNED32 COB_IDClientToServer;
	UNSIGNED32 COB_IDServerToClient;
	UNSIGNED8 nodeIDOfTheSDOServer;
}              OD_SDOClientParameter_t;
/*1400    */ typedef struct {
	UNSIGNED8 maxSubIndex;
	UNSIGNED32 COB_IDUsedByRPDO;
	UNSIGNED8 transmissionType;
}              OD_RPDOCommunicationParameter_t;
/*1600    */ typedef struct {
	UNSIGNED8 numberOfMappedObjects;
	UNSIGNED32 mappedObject1;
	UNSIGNED32 mappedObject2;
	UNSIGNED32 mappedObject3;
	UNSIGNED32 mappedObject4;
	UNSIGNED32 mappedObject5;
	UNSIGNED32 mappedObject6;
	UNSIGNED32 mappedObject7;
	UNSIGNED32 mappedObject8;
}              OD_RPDOMappingParameter_t;
/*1800    */ typedef struct {
	UNSIGNED8 maxSubIndex;
	UNSIGNED32 COB_IDUsedByTPDO;
	UNSIGNED8 transmissionType;
	UNSIGNED16 inhibitTime;
	UNSIGNED8 compatibilityEntry;
	UNSIGNED16 eventTimer;
	UNSIGNED8 SYNCStartValue;
}              OD_TPDOCommunicationParameter_t;
/*1a00    */ typedef struct {
	UNSIGNED8 numberOfMappedObjects;
	UNSIGNED32 mappedObject1;
	UNSIGNED32 mappedObject2;
	UNSIGNED32 mappedObject3;
	UNSIGNED32 mappedObject4;
	UNSIGNED32 mappedObject5;
	UNSIGNED32 mappedObject6;
	UNSIGNED32 mappedObject7;
	UNSIGNED32 mappedObject8;
}              OD_TPDOMappingParameter_t;

/*******************************************************************************
   TYPE DEFINITIONS FOR OBJECT DICTIONARY INDEXES

   some of those are redundant with CO_SDO.h CO_ObjDicId_t <Common CiA301 object
   dictionary entries>
*******************************************************************************/
/*1000 */
	#define OD_1000_deviceType                                  0x1000

/*1001 */
	#define OD_1001_errorRegister                               0x1001

/*1002 */
	#define OD_1002_manufacturerStatusRegister                  0x1002

/*1003 */
	#define OD_1003_preDefinedErrorField                        0x1003

	#define OD_1003_0_preDefinedErrorField_maxSubIndex          0
	#define OD_1003_1_preDefinedErrorField_standardErrorField   1
	#define OD_1003_2_preDefinedErrorField_standardErrorField   2
	#define OD_1003_3_preDefinedErrorField_standardErrorField   3
	#define OD_1003_4_preDefinedErrorField_standardErrorField   4
	#define OD_1003_5_preDefinedErrorField_standardErrorField   5
	#define OD_1003_6_preDefinedErrorField_standardErrorField   6
	#define OD_1003_7_preDefinedErrorField_standardErrorField   7
	#define OD_1003_8_preDefinedErrorField_standardErrorField   8

/*1005 */
	#define OD_1005_COB_ID_SYNCMessage                          0x1005

/*1006 */
	#define OD_1006_communicationCyclePeriod                    0x1006

/*1007 */
	#define OD_1007_synchronousWindowLength                     0x1007

/*1008 */
	#define OD_1008_manufacturerDeviceName                      0x1008

/*1009 */
	#define OD_1009_manufacturerHardwareVersion                 0x1009

/*100a */
	#define OD_100a_manufacturerSoftwareVersion                 0x100a

/*1010 */
	#define OD_1010_storeParameters                             0x1010

	#define OD_1010_0_storeParameters_maxSubIndex               0
	#define OD_1010_1_storeParameters_saveAllParameters         1

/*1011 */
	#define OD_1011_restoreDefaultParameters                    0x1011

	#define OD_1011_0_restoreDefaultParameters_maxSubIndex      0
	#define OD_1011_1_restoreDefaultParameters_restoreAllDefaultParameters 1

/*1012 */
	#define OD_1012_COB_ID_TIME                                 0x1012

/*1014 */
	#define OD_1014_COB_ID_EMCY                                 0x1014

/*1015 */
	#define OD_1015_inhibitTimeEMCY                             0x1015

/*1016 */
	#define OD_1016_consumerHeartbeatTime                       0x1016

	#define OD_1016_0_consumerHeartbeatTime_maxSubIndex         0
	#define OD_1016_1_consumerHeartbeatTime_consumerHeartbeatTime 1
	#define OD_1016_2_consumerHeartbeatTime_consumerHeartbeatTime 2
	#define OD_1016_3_consumerHeartbeatTime_consumerHeartbeatTime 3
	#define OD_1016_4_consumerHeartbeatTime_consumerHeartbeatTime 4

/*1017 */
	#define OD_1017_producerHeartbeatTime                       0x1017

/*1018 */
	#define OD_1018_identity                                    0x1018

	#define OD_1018_0_identity_maxSubIndex                      0
	#define OD_1018_1_identity_vendorID                         1
	#define OD_1018_2_identity_productCode                      2
	#define OD_1018_3_identity_revisionNumber                   3
	#define OD_1018_4_identity_serialNumber                     4

/*1019 */
	#define OD_1019_synchronousCounterOverflowValue             0x1019

/*1029 */
	#define OD_1029_errorBehavior                               0x1029

	#define OD_1029_0_errorBehavior_maxSubIndex                 0
	#define OD_1029_1_errorBehavior_communication               1
	#define OD_1029_2_errorBehavior_communicationOther          2
	#define OD_1029_3_errorBehavior_communicationPassive        3
	#define OD_1029_4_errorBehavior_generic                     4
	#define OD_1029_5_errorBehavior_deviceProfile               5
	#define OD_1029_6_errorBehavior_manufacturerSpecific        6

/*1200 */
	#define OD_1200_SDOServerParameter                          0x1200

	#define OD_1200_0_SDOServerParameter_maxSubIndex            0
	#define OD_1200_1_SDOServerParameter_COB_IDClientToServer   1
	#define OD_1200_2_SDOServerParameter_COB_IDServerToClient   2

/*1400 */
	#define OD_1400_RPDOCommunicationParameter                  0x1400

	#define OD_1400_0_RPDOCommunicationParameter_maxSubIndex    0
	#define OD_1400_1_RPDOCommunicationParameter_COB_IDUsedByRPDO 1
	#define OD_1400_2_RPDOCommunicationParameter_transmissionType 2

/*1401 */
	#define OD_1401_RPDOCommunicationParameter                  0x1401

	#define OD_1401_0_RPDOCommunicationParameter_maxSubIndex    0
	#define OD_1401_1_RPDOCommunicationParameter_COB_IDUsedByRPDO 1
	#define OD_1401_2_RPDOCommunicationParameter_transmissionType 2

/*1402 */
	#define OD_1402_RPDOCommunicationParameter                  0x1402

	#define OD_1402_0_RPDOCommunicationParameter_maxSubIndex    0
	#define OD_1402_1_RPDOCommunicationParameter_COB_IDUsedByRPDO 1
	#define OD_1402_2_RPDOCommunicationParameter_transmissionType 2

/*1403 */
	#define OD_1403_RPDOCommunicationParameter                  0x1403

	#define OD_1403_0_RPDOCommunicationParameter_maxSubIndex    0
	#define OD_1403_1_RPDOCommunicationParameter_COB_IDUsedByRPDO 1
	#define OD_1403_2_RPDOCommunicationParameter_transmissionType 2

/*1600 */
	#define OD_1600_RPDOMappingParameter                        0x1600

	#define OD_1600_0_RPDOMappingParameter_maxSubIndex          0
	#define OD_1600_1_RPDOMappingParameter_mappedObject1        1
	#define OD_1600_2_RPDOMappingParameter_mappedObject2        2
	#define OD_1600_3_RPDOMappingParameter_mappedObject3        3
	#define OD_1600_4_RPDOMappingParameter_mappedObject4        4
	#define OD_1600_5_RPDOMappingParameter_mappedObject5        5
	#define OD_1600_6_RPDOMappingParameter_mappedObject6        6
	#define OD_1600_7_RPDOMappingParameter_mappedObject7        7
	#define OD_1600_8_RPDOMappingParameter_mappedObject8        8

/*1601 */
	#define OD_1601_RPDOMappingParameter                        0x1601

	#define OD_1601_0_RPDOMappingParameter_maxSubIndex          0
	#define OD_1601_1_RPDOMappingParameter_mappedObject1        1
	#define OD_1601_2_RPDOMappingParameter_mappedObject2        2
	#define OD_1601_3_RPDOMappingParameter_mappedObject3        3
	#define OD_1601_4_RPDOMappingParameter_mappedObject4        4
	#define OD_1601_5_RPDOMappingParameter_mappedObject5        5
	#define OD_1601_6_RPDOMappingParameter_mappedObject6        6
	#define OD_1601_7_RPDOMappingParameter_mappedObject7        7
	#define OD_1601_8_RPDOMappingParameter_mappedObject8        8

/*1602 */
	#define OD_1602_RPDOMappingParameter                        0x1602

	#define OD_1602_0_RPDOMappingParameter_maxSubIndex          0
	#define OD_1602_1_RPDOMappingParameter_mappedObject1        1
	#define OD_1602_2_RPDOMappingParameter_mappedObject2        2
	#define OD_1602_3_RPDOMappingParameter_mappedObject3        3
	#define OD_1602_4_RPDOMappingParameter_mappedObject4        4
	#define OD_1602_5_RPDOMappingParameter_mappedObject5        5
	#define OD_1602_6_RPDOMappingParameter_mappedObject6        6
	#define OD_1602_7_RPDOMappingParameter_mappedObject7        7
	#define OD_1602_8_RPDOMappingParameter_mappedObject8        8

/*1603 */
	#define OD_1603_RPDOMappingParameter                        0x1603

	#define OD_1603_0_RPDOMappingParameter_maxSubIndex          0
	#define OD_1603_1_RPDOMappingParameter_mappedObject1        1
	#define OD_1603_2_RPDOMappingParameter_mappedObject2        2
	#define OD_1603_3_RPDOMappingParameter_mappedObject3        3
	#define OD_1603_4_RPDOMappingParameter_mappedObject4        4
	#define OD_1603_5_RPDOMappingParameter_mappedObject5        5
	#define OD_1603_6_RPDOMappingParameter_mappedObject6        6
	#define OD_1603_7_RPDOMappingParameter_mappedObject7        7
	#define OD_1603_8_RPDOMappingParameter_mappedObject8        8

/*1800 */
	#define OD_1800_TPDOCommunicationParameter                  0x1800

	#define OD_1800_0_TPDOCommunicationParameter_maxSubIndex    0
	#define OD_1800_1_TPDOCommunicationParameter_COB_IDUsedByTPDO 1
	#define OD_1800_2_TPDOCommunicationParameter_transmissionType 2
	#define OD_1800_3_TPDOCommunicationParameter_inhibitTime    3
	#define OD_1800_4_TPDOCommunicationParameter_compatibilityEntry 4
	#define OD_1800_5_TPDOCommunicationParameter_eventTimer     5
	#define OD_1800_6_TPDOCommunicationParameter_SYNCStartValue 6

/*1801 */
	#define OD_1801_TPDOCommunicationParameter                  0x1801

	#define OD_1801_0_TPDOCommunicationParameter_maxSubIndex    0
	#define OD_1801_1_TPDOCommunicationParameter_COB_IDUsedByTPDO 1
	#define OD_1801_2_TPDOCommunicationParameter_transmissionType 2
	#define OD_1801_3_TPDOCommunicationParameter_inhibitTime    3
	#define OD_1801_4_TPDOCommunicationParameter_compatibilityEntry 4
	#define OD_1801_5_TPDOCommunicationParameter_eventTimer     5
	#define OD_1801_6_TPDOCommunicationParameter_SYNCStartValue 6

/*1802 */
	#define OD_1802_TPDOCommunicationParameter                  0x1802

	#define OD_1802_0_TPDOCommunicationParameter_maxSubIndex    0
	#define OD_1802_1_TPDOCommunicationParameter_COB_IDUsedByTPDO 1
	#define OD_1802_2_TPDOCommunicationParameter_transmissionType 2
	#define OD_1802_3_TPDOCommunicationParameter_inhibitTime    3
	#define OD_1802_4_TPDOCommunicationParameter_compatibilityEntry 4
	#define OD_1802_5_TPDOCommunicationParameter_eventTimer     5
	#define OD_1802_6_TPDOCommunicationParameter_SYNCStartValue 6

/*1803 */
	#define OD_1803_TPDOCommunicationParameter                  0x1803

	#define OD_1803_0_TPDOCommunicationParameter_maxSubIndex    0
	#define OD_1803_1_TPDOCommunicationParameter_COB_IDUsedByTPDO 1
	#define OD_1803_2_TPDOCommunicationParameter_transmissionType 2
	#define OD_1803_3_TPDOCommunicationParameter_inhibitTime    3
	#define OD_1803_4_TPDOCommunicationParameter_compatibilityEntry 4
	#define OD_1803_5_TPDOCommunicationParameter_eventTimer     5
	#define OD_1803_6_TPDOCommunicationParameter_SYNCStartValue 6

/*1804 */
	#define OD_1804_TPDOCommunicationParameter                  0x1804

	#define OD_1804_0_TPDOCommunicationParameter_maxSubIndex    0
	#define OD_1804_1_TPDOCommunicationParameter_COB_IDUsedByTPDO 1
	#define OD_1804_2_TPDOCommunicationParameter_transmissionType 2
	#define OD_1804_3_TPDOCommunicationParameter_inhibitTime    3
	#define OD_1804_4_TPDOCommunicationParameter_compatibilityEntry 4
	#define OD_1804_5_TPDOCommunicationParameter_eventTimer     5
	#define OD_1804_6_TPDOCommunicationParameter_SYNCStartValue 6

/*1a00 */
	#define OD_1a00_TPDOMappingParameter                        0x1a00

	#define OD_1a00_0_TPDOMappingParameter_maxSubIndex          0
	#define OD_1a00_1_TPDOMappingParameter_mappedObject1        1
	#define OD_1a00_2_TPDOMappingParameter_mappedObject2        2
	#define OD_1a00_3_TPDOMappingParameter_mappedObject3        3
	#define OD_1a00_4_TPDOMappingParameter_mappedObject4        4
	#define OD_1a00_5_TPDOMappingParameter_mappedObject5        5
	#define OD_1a00_6_TPDOMappingParameter_mappedObject6        6
	#define OD_1a00_7_TPDOMappingParameter_mappedObject7        7
	#define OD_1a00_8_TPDOMappingParameter_mappedObject8        8

/*1a01 */
	#define OD_1a01_TPDOMappingParameter                        0x1a01

	#define OD_1a01_0_TPDOMappingParameter_maxSubIndex          0
	#define OD_1a01_1_TPDOMappingParameter_mappedObject1        1
	#define OD_1a01_2_TPDOMappingParameter_mappedObject2        2
	#define OD_1a01_3_TPDOMappingParameter_mappedObject3        3
	#define OD_1a01_4_TPDOMappingParameter_mappedObject4        4
	#define OD_1a01_5_TPDOMappingParameter_mappedObject5        5
	#define OD_1a01_6_TPDOMappingParameter_mappedObject6        6
	#define OD_1a01_7_TPDOMappingParameter_mappedObject7        7
	#define OD_1a01_8_TPDOMappingParameter_mappedObject8        8

/*1a02 */
	#define OD_1a02_TPDOMappingParameter                        0x1a02

	#define OD_1a02_0_TPDOMappingParameter_maxSubIndex          0
	#define OD_1a02_1_TPDOMappingParameter_mappedObject1        1
	#define OD_1a02_2_TPDOMappingParameter_mappedObject2        2
	#define OD_1a02_3_TPDOMappingParameter_mappedObject3        3
	#define OD_1a02_4_TPDOMappingParameter_mappedObject4        4
	#define OD_1a02_5_TPDOMappingParameter_mappedObject5        5
	#define OD_1a02_6_TPDOMappingParameter_mappedObject6        6
	#define OD_1a02_7_TPDOMappingParameter_mappedObject7        7
	#define OD_1a02_8_TPDOMappingParameter_mappedObject8        8

/*1a03 */
	#define OD_1a03_TPDOMappingParameter                        0x1a03

	#define OD_1a03_0_TPDOMappingParameter_maxSubIndex          0
	#define OD_1a03_1_TPDOMappingParameter_mappedObject1        1
	#define OD_1a03_2_TPDOMappingParameter_mappedObject2        2
	#define OD_1a03_3_TPDOMappingParameter_mappedObject3        3
	#define OD_1a03_4_TPDOMappingParameter_mappedObject4        4
	#define OD_1a03_5_TPDOMappingParameter_mappedObject5        5
	#define OD_1a03_6_TPDOMappingParameter_mappedObject6        6
	#define OD_1a03_7_TPDOMappingParameter_mappedObject7        7
	#define OD_1a03_8_TPDOMappingParameter_mappedObject8        8

/*1a04 */
	#define OD_1a04_TPDOMappingParameter                        0x1a04

	#define OD_1a04_0_TPDOMappingParameter_maxSubIndex          0
	#define OD_1a04_1_TPDOMappingParameter_mappedObject1        1
	#define OD_1a04_2_TPDOMappingParameter_mappedObject2        2
	#define OD_1a04_3_TPDOMappingParameter_mappedObject3        3
	#define OD_1a04_4_TPDOMappingParameter_mappedObject4        4
	#define OD_1a04_5_TPDOMappingParameter_mappedObject5        5
	#define OD_1a04_6_TPDOMappingParameter_mappedObject6        6
	#define OD_1a04_7_TPDOMappingParameter_mappedObject7        7
	#define OD_1a04_8_TPDOMappingParameter_mappedObject8        8

/*1f50 */
	#define OD_1f50_programData                                 0x1f50

	#define OD_1f50_0_programData_maxSubIndex                   0
	#define OD_1f50_1_programData_                              1

/*1f51 */
	#define OD_1f51_programControl                              0x1f51

	#define OD_1f51_0_programControl_maxSubIndex                0
	#define OD_1f51_1_programControl_                           1

/*1f56 */
	#define OD_1f56_programSoftwareIdentification               0x1f56

	#define OD_1f56_0_programSoftwareIdentification_maxSubIndex 0
	#define OD_1f56_1_programSoftwareIdentification_            1

/*1f57 */
	#define OD_1f57_flashStatusIdentification                   0x1f57

	#define OD_1f57_0_flashStatusIdentification_maxSubIndex     0
	#define OD_1f57_1_flashStatusIdentification_                1

/*1f80 */
	#define OD_1f80_NMTStartup                                  0x1f80

/*2000 */
	#define OD_2000_outputStates                                0x2000

/*2001 */
	#define OD_2001_outputCommanded                             0x2001

/*2002 */
	#define OD_2002_outputFaults                                0x2002

/*2003 */
	#define OD_2003_overCurrentFaults                           0x2003

/*2004 */
	#define OD_2004_openLoadFaults                              0x2004

/*2005 */
	#define OD_2005_outputDisabled                              0x2005

/*2006 */
	#define OD_2006_totalCurrent_mA                             0x2006

/*2007 */
	#define OD_2007_supplyVoltage_mV                            0x2007

/*2008 */
	#define OD_2008_boardTemperature_dC                         0x2008

/*2009 */
	#define OD_2009_mcuTemperature_dC                           0x2009

/*200a */
	#define OD_200a_uptime_s                                    0x200a

/*200b */
	#define OD_200b_resetReason                                 0x200b

/*200c */
	#define OD_200c_brownoutCount                               0x200c

/*200d */
	#define OD_200d_canBusOffCount                              0x200d

/*200e */
	#define OD_200e_warningFlags                                0x200e

/*200f */
	#define OD_200f_telemetryValidity                           0x200f

/*2010 */
	#define OD_2010_mcuSupplyVoltage_mV                         0x2010

/*2100 */
	#define OD_2100_errorStatusBits                             0x2100

/*2101 */
	#define OD_2101_powerOnCounter                              0x2101

/*2102 */
	#define OD_2102_buttonPressCounter                          0x2102

/*2103 */
	#define OD_2103_outputRequest                               0x2103

/*2104 */
	#define OD_2104_faultClearRequest                           0x2104

/*2105 */
	#define OD_2105_pendingNodeID                               0x2105

/*2106 */
	#define OD_2106_pendingBitrate_kbps                         0x2106

/*2107 */
	#define OD_2107_commApply                                   0x2107

/*3000 */
	#define OD_3000_outputCurrent_mA                            0x3000

/*3001 */
	#define OD_3001_currentSenseRaw                             0x3001

/*3002 */
	#define OD_3002_peakCurrent_mA                              0x3002

/*3003 */
	#define OD_3003_overCurrentTripCount                        0x3003

/*3100 */
	#define OD_3100_currentLimit_mA                             0x3100

/*3101 */
	#define OD_3101_currentTripTime_ms                          0x3101

/*3102 */
	#define OD_3102_inrushLimit_mA                              0x3102

/*3103 */
	#define OD_3103_inrushTime_ms                               0x3103

/*******************************************************************************
   STRUCTURES FOR VARIABLES IN DIFFERENT MEMORY LOCATIONS
*******************************************************************************/
#define  CO_OD_FIRST_LAST_WORD     0x55 /* Any value from 0x01 to 0xFE. If changed, EEPROM will be reinitialized. */

/***** Structure for ROM variables ********************************************/
struct sCO_OD_ROM {
	UNSIGNED32 FirstWord;

/*1000      */ UNSIGNED32 deviceType;
/*1005      */ UNSIGNED32 COB_ID_SYNCMessage;
/*1006      */ UNSIGNED32 communicationCyclePeriod;
/*1007      */ UNSIGNED32 synchronousWindowLength;
/*1008      */ VISIBLE_STRING manufacturerDeviceName[14];
/*1009      */ VISIBLE_STRING manufacturerHardwareVersion[4];
/*100a      */ VISIBLE_STRING manufacturerSoftwareVersion[4];
/*1012      */ UNSIGNED32 COB_ID_TIME;
/*1014      */ UNSIGNED32 COB_ID_EMCY;
/*1015      */ UNSIGNED16 inhibitTimeEMCY;
/*1016      */ UNSIGNED32 consumerHeartbeatTime[4];
/*1017      */ UNSIGNED16 producerHeartbeatTime;
/*1018      */ OD_identity_t identity;
/*1019      */ UNSIGNED8 synchronousCounterOverflowValue;
/*1029      */ UNSIGNED8 errorBehavior[6];
/*1200      */ OD_SDOServerParameter_t SDOServerParameter[1];
/*1400      */ OD_RPDOCommunicationParameter_t RPDOCommunicationParameter[4];
/*1600      */ OD_RPDOMappingParameter_t RPDOMappingParameter[4];
/*1800      */ OD_TPDOCommunicationParameter_t TPDOCommunicationParameter[5];
/*1a00      */ OD_TPDOMappingParameter_t TPDOMappingParameter[5];
/*1f80      */ UNSIGNED32 NMTStartup;

	UNSIGNED32 LastWord;
};

/***** Structure for RAM variables ********************************************/
struct sCO_OD_RAM {
	UNSIGNED32 FirstWord;

/*1001      */ UNSIGNED8 errorRegister;
/*1002      */ UNSIGNED32 manufacturerStatusRegister;
/*1003      */ UNSIGNED32 preDefinedErrorField[8];
/*1010      */ UNSIGNED32 storeParameters[1];
/*1011      */ UNSIGNED32 restoreDefaultParameters[1];
/*1f50      */ DOMAIN programData[1];
/*1f51      */ UNSIGNED8 programControl[1];
/*1f56      */ UNSIGNED32 programSoftwareIdentification[1];
/*1f57      */ UNSIGNED32 flashStatusIdentification[1];
/*2000      */ UNSIGNED16 outputStates;
/*2001      */ UNSIGNED16 outputCommanded;
/*2002      */ UNSIGNED16 outputFaults;
/*2003      */ UNSIGNED16 overCurrentFaults;
/*2004      */ UNSIGNED16 openLoadFaults;
/*2005      */ UNSIGNED16 outputDisabled;
/*2006      */ UNSIGNED32 totalCurrent_mA;
/*2007      */ UNSIGNED16 supplyVoltage_mV;
/*2008      */ INTEGER16 boardTemperature_dC;
/*2009      */ INTEGER16 mcuTemperature_dC;
/*200a      */ UNSIGNED32 uptime_s;
/*200b      */ UNSIGNED16 resetReason;
/*200c      */ UNSIGNED16 brownoutCount;
/*200d      */ UNSIGNED16 canBusOffCount;
/*200e      */ UNSIGNED16 warningFlags;
/*200f      */ UNSIGNED32 telemetryValidity;
/*2010      */ UNSIGNED16 mcuSupplyVoltage_mV;
/*2100      */ OCTET_STRING errorStatusBits[10];
/*2102      */ UNSIGNED32 buttonPressCounter;
/*2103      */ UNSIGNED16 outputRequest;
/*2104      */ UNSIGNED16 faultClearRequest;
/*2105      */ UNSIGNED8 pendingNodeID;
/*2106      */ UNSIGNED16 pendingBitrate_kbps;
/*2107      */ UNSIGNED8 commApply;
/*3000      */ UNSIGNED16 outputCurrent_mA[15];
/*3001      */ UNSIGNED16 currentSenseRaw[15];
/*3002      */ UNSIGNED16 peakCurrent_mA[15];
/*3003      */ UNSIGNED32 overCurrentTripCount[15];
/*3100      */ UNSIGNED16 currentLimit_mA[15];
/*3101      */ UNSIGNED16 currentTripTime_ms[15];
/*3102      */ UNSIGNED16 inrushLimit_mA[15];
/*3103      */ UNSIGNED16 inrushTime_ms[15];

	UNSIGNED32 LastWord;
};

/***** Structure for EEPROM variables ********************************************/
struct sCO_OD_EEPROM {
	UNSIGNED32 FirstWord;

/*2101      */ UNSIGNED32 powerOnCounter;

	UNSIGNED32 LastWord;
};

/***** Declaration of Object Dictionary variables *****************************/
extern struct sCO_OD_ROM CO_OD_ROM;

extern struct sCO_OD_RAM CO_OD_RAM;

extern struct sCO_OD_EEPROM CO_OD_EEPROM;

/*******************************************************************************
   ALIASES FOR OBJECT DICTIONARY VARIABLES
*******************************************************************************/
/*1000, Data Type: UNSIGNED32 */
	#define OD_deviceType                                       CO_OD_ROM.deviceType

/*1001, Data Type: UNSIGNED8 */
	#define OD_errorRegister                                    CO_OD_RAM.errorRegister

/*1002, Data Type: UNSIGNED32 */
	#define OD_manufacturerStatusRegister                       CO_OD_RAM.manufacturerStatusRegister

/*1003, Data Type: UNSIGNED32, Array[8] */
	#define OD_preDefinedErrorField                             CO_OD_RAM.preDefinedErrorField
	#define ODL_preDefinedErrorField_arrayLength                8
	#define ODA_preDefinedErrorField_standardErrorField         0

/*1005, Data Type: UNSIGNED32 */
	#define OD_COB_ID_SYNCMessage                               CO_OD_ROM.COB_ID_SYNCMessage

/*1006, Data Type: UNSIGNED32 */
	#define OD_communicationCyclePeriod                         CO_OD_ROM.communicationCyclePeriod

/*1007, Data Type: UNSIGNED32 */
	#define OD_synchronousWindowLength                          CO_OD_ROM.synchronousWindowLength

/*1008, Data Type: VISIBLE_STRING */
	#define OD_manufacturerDeviceName                           CO_OD_ROM.manufacturerDeviceName
	#define ODL_manufacturerDeviceName_stringLength             14

/*1009, Data Type: VISIBLE_STRING */
	#define OD_manufacturerHardwareVersion                      CO_OD_ROM.manufacturerHardwareVersion
	#define ODL_manufacturerHardwareVersion_stringLength        4

/*100a, Data Type: VISIBLE_STRING */
	#define OD_manufacturerSoftwareVersion                      CO_OD_ROM.manufacturerSoftwareVersion
	#define ODL_manufacturerSoftwareVersion_stringLength        4

/*1010, Data Type: UNSIGNED32, Array[1] */
	#define OD_storeParameters                                  CO_OD_RAM.storeParameters
	#define ODL_storeParameters_arrayLength                     1
	#define ODA_storeParameters_saveAllParameters               0

/*1011, Data Type: UNSIGNED32, Array[1] */
	#define OD_restoreDefaultParameters                         CO_OD_RAM.restoreDefaultParameters
	#define ODL_restoreDefaultParameters_arrayLength            1
	#define ODA_restoreDefaultParameters_restoreAllDefaultParameters 0

/*1012, Data Type: UNSIGNED32 */
	#define OD_COB_ID_TIME                                      CO_OD_ROM.COB_ID_TIME

/*1014, Data Type: UNSIGNED32 */
	#define OD_COB_ID_EMCY                                      CO_OD_ROM.COB_ID_EMCY

/*1015, Data Type: UNSIGNED16 */
	#define OD_inhibitTimeEMCY                                  CO_OD_ROM.inhibitTimeEMCY

/*1016, Data Type: UNSIGNED32, Array[4] */
	#define OD_consumerHeartbeatTime                            CO_OD_ROM.consumerHeartbeatTime
	#define ODL_consumerHeartbeatTime_arrayLength               4
	#define ODA_consumerHeartbeatTime_consumerHeartbeatTime     0

/*1017, Data Type: UNSIGNED16 */
	#define OD_producerHeartbeatTime                            CO_OD_ROM.producerHeartbeatTime

/*1018, Data Type: identity_t */
	#define OD_identity                                         CO_OD_ROM.identity

/*1019, Data Type: UNSIGNED8 */
	#define OD_synchronousCounterOverflowValue                  CO_OD_ROM.synchronousCounterOverflowValue

/*1029, Data Type: UNSIGNED8, Array[6] */
	#define OD_errorBehavior                                    CO_OD_ROM.errorBehavior
	#define ODL_errorBehavior_arrayLength                       6
	#define ODA_errorBehavior_communication                     0
	#define ODA_errorBehavior_communicationOther                1
	#define ODA_errorBehavior_communicationPassive              2
	#define ODA_errorBehavior_generic                           3
	#define ODA_errorBehavior_deviceProfile                     4
	#define ODA_errorBehavior_manufacturerSpecific              5

/*1200, Data Type: SDOServerParameter_t */
	#define OD_SDOServerParameter                               CO_OD_ROM.SDOServerParameter

/*1400, Data Type: RPDOCommunicationParameter_t */
	#define OD_RPDOCommunicationParameter                       CO_OD_ROM.RPDOCommunicationParameter

/*1600, Data Type: RPDOMappingParameter_t */
	#define OD_RPDOMappingParameter                             CO_OD_ROM.RPDOMappingParameter

/*1800, Data Type: TPDOCommunicationParameter_t */
	#define OD_TPDOCommunicationParameter                       CO_OD_ROM.TPDOCommunicationParameter

/*1a00, Data Type: TPDOMappingParameter_t */
	#define OD_TPDOMappingParameter                             CO_OD_ROM.TPDOMappingParameter

/*1f50, Data Type: DOMAIN, Array[1] */
	#define OD_programData                                      CO_OD_RAM.programData
	#define ODL_programData_arrayLength                         1
	#define ODA_programData_                                    0

/*1f51, Data Type: UNSIGNED8, Array[1] */
	#define OD_programControl                                   CO_OD_RAM.programControl
	#define ODL_programControl_arrayLength                      1
	#define ODA_programControl_                                 0

/*1f56, Data Type: UNSIGNED32, Array[1] */
	#define OD_programSoftwareIdentification                    CO_OD_RAM.programSoftwareIdentification
	#define ODL_programSoftwareIdentification_arrayLength       1
	#define ODA_programSoftwareIdentification_                  0

/*1f57, Data Type: UNSIGNED32, Array[1] */
	#define OD_flashStatusIdentification                        CO_OD_RAM.flashStatusIdentification
	#define ODL_flashStatusIdentification_arrayLength           1
	#define ODA_flashStatusIdentification_                      0

/*1f80, Data Type: UNSIGNED32 */
	#define OD_NMTStartup                                       CO_OD_ROM.NMTStartup

/*2000, Data Type: UNSIGNED16 */
	#define OD_outputStates                                     CO_OD_RAM.outputStates

/*2001, Data Type: UNSIGNED16 */
	#define OD_outputCommanded                                  CO_OD_RAM.outputCommanded

/*2002, Data Type: UNSIGNED16 */
	#define OD_outputFaults                                     CO_OD_RAM.outputFaults

/*2003, Data Type: UNSIGNED16 */
	#define OD_overCurrentFaults                                CO_OD_RAM.overCurrentFaults

/*2004, Data Type: UNSIGNED16 */
	#define OD_openLoadFaults                                   CO_OD_RAM.openLoadFaults

/*2005, Data Type: UNSIGNED16 */
	#define OD_outputDisabled                                   CO_OD_RAM.outputDisabled

/*2006, Data Type: UNSIGNED32 */
	#define OD_totalCurrent_mA                                  CO_OD_RAM.totalCurrent_mA

/*2007, Data Type: UNSIGNED16 */
	#define OD_supplyVoltage_mV                                 CO_OD_RAM.supplyVoltage_mV

/*2008, Data Type: INTEGER16 */
	#define OD_boardTemperature_dC                              CO_OD_RAM.boardTemperature_dC

/*2009, Data Type: INTEGER16 */
	#define OD_mcuTemperature_dC                                CO_OD_RAM.mcuTemperature_dC

/*200a, Data Type: UNSIGNED32 */
	#define OD_uptime_s                                         CO_OD_RAM.uptime_s

/*200b, Data Type: UNSIGNED16 */
	#define OD_resetReason                                      CO_OD_RAM.resetReason

/*200c, Data Type: UNSIGNED16 */
	#define OD_brownoutCount                                    CO_OD_RAM.brownoutCount

/*200d, Data Type: UNSIGNED16 */
	#define OD_canBusOffCount                                   CO_OD_RAM.canBusOffCount

/*200e, Data Type: UNSIGNED16 */
	#define OD_warningFlags                                     CO_OD_RAM.warningFlags

/*200f, Data Type: UNSIGNED32 */
	#define OD_telemetryValidity                                CO_OD_RAM.telemetryValidity

/*2010, Data Type: UNSIGNED16 */
	#define OD_mcuSupplyVoltage_mV                              CO_OD_RAM.mcuSupplyVoltage_mV

/*2100, Data Type: OCTET_STRING */
	#define OD_errorStatusBits                                  CO_OD_RAM.errorStatusBits
	#define ODL_errorStatusBits_stringLength                    10

/*2101, Data Type: UNSIGNED32 */
	#define OD_powerOnCounter                                   CO_OD_EEPROM.powerOnCounter

/*2102, Data Type: UNSIGNED32 */
	#define OD_buttonPressCounter                               CO_OD_RAM.buttonPressCounter

/*2103, Data Type: UNSIGNED16 */
	#define OD_outputRequest                                    CO_OD_RAM.outputRequest

/*2104, Data Type: UNSIGNED16 */
	#define OD_faultClearRequest                                CO_OD_RAM.faultClearRequest

/*2105, Data Type: UNSIGNED8 */
	#define OD_pendingNodeID                                    CO_OD_RAM.pendingNodeID

/*2106, Data Type: UNSIGNED16 */
	#define OD_pendingBitrate_kbps                              CO_OD_RAM.pendingBitrate_kbps

/*2107, Data Type: UNSIGNED8 */
	#define OD_commApply                                        CO_OD_RAM.commApply

/*3000, Data Type: UNSIGNED16, Array[15] */
	#define OD_outputCurrent_mA                                 CO_OD_RAM.outputCurrent_mA
	#define ODL_outputCurrent_mA_arrayLength                    15

/*3001, Data Type: UNSIGNED16, Array[15] */
	#define OD_currentSenseRaw                                  CO_OD_RAM.currentSenseRaw
	#define ODL_currentSenseRaw_arrayLength                     15

/*3002, Data Type: UNSIGNED16, Array[15] */
	#define OD_peakCurrent_mA                                   CO_OD_RAM.peakCurrent_mA
	#define ODL_peakCurrent_mA_arrayLength                      15

/*3003, Data Type: UNSIGNED32, Array[15] */
	#define OD_overCurrentTripCount                             CO_OD_RAM.overCurrentTripCount
	#define ODL_overCurrentTripCount_arrayLength                15

/*3100, Data Type: UNSIGNED16, Array[15] */
	#define OD_currentLimit_mA                                  CO_OD_RAM.currentLimit_mA
	#define ODL_currentLimit_mA_arrayLength                     15

/*3101, Data Type: UNSIGNED16, Array[15] */
	#define OD_currentTripTime_ms                               CO_OD_RAM.currentTripTime_ms
	#define ODL_currentTripTime_ms_arrayLength                  15

/*3102, Data Type: UNSIGNED16, Array[15] */
	#define OD_inrushLimit_mA                                   CO_OD_RAM.inrushLimit_mA
	#define ODL_inrushLimit_mA_arrayLength                      15

/*3103, Data Type: UNSIGNED16, Array[15] */
	#define OD_inrushTime_ms                                    CO_OD_RAM.inrushTime_ms
	#define ODL_inrushTime_ms_arrayLength                       15

#endif
