# Copyright 2023 Engineerang <engineerang@jpodtech.com>
# SPDX-License-Identifier: Apache-2.0

from ctypes import c_char, Structure

CID_WB_1000 = 1
CID_WB_4000 = 2
CID_HAM_0030 = 3
CID_HAM_0070 = 4
CID_HAM_0145 = 5
CID_HAM_0220 = 6
CID_HAM_0435 = 7
CID_HAM_0920 = 8
CID_HAM_1280 = 9
CID_HAM_2400 = 10
CID_HAM_3500 = 11
CID_CELL_BAND01 = 12
CID_CELL_BAND02 = 13
CID_CELL_BAND03 = 14
CID_CELL_BAND07 = 15
CID_CELL_BAND38 = 16
CID_AUTO = -2
CID_NOT_SELECTED = 100

# LimeRFE convenience constants for notch on/off control
NOTCH_VALUE_OFF = 0
NOTCH_VALUE_ON = 1

MODE_RX = 0     # RX - Enabled;  TX - Disabled
MODE_TX = 1     # RX - Disabled; TX - Enabled
MODE_NONE = 2   # RX - Disabled; TX - Disabled
MODE_TXRX = 3   # RX - Enabled;  TX - Enabled

PORT_1 = 1      # Connector J3 - 'TX/RX'
PORT_2 = 2      # Connector J4 - 'TX'
PORT_3 = 3      # Connector J5 - '30 MHz TX/RX'

# LimeRFE SWR subsystem enable
ENABLESWR = 1
DISABLESWR = 0

# LimeRFE SWR subsystem source
SWR_SRC_EXT = 0     # External - SWR signals are supplied to the connectors J18 for forward and J17 for forward signal. To be supplied from the external coupler.
SWR_SRC_CELL = 1    # Cellular - Power Meter signal is provided internally from the cellular TX amplifier outputs.

#LimeRFE error codes
def checkReturnCodes(code):
    return_codes = {
        0: 'SUCCESS',                       # Success
        -4: 'ERROR_COMM_SYNC',	            # <Error synchronizing communication
        -3: 'ERROR_GPIO_PIN', 	            # <Non-configurable GPIO pin specified. Only pins 4 and 5 are configurable.
        -2: 'ERROR_CONF_FILE',	            # <Problem with .ini configuration file
        -1: 'ERROR_COMM',	                # <Communication error
        1: 'ERROR_INCORRECT_TX_CONN',	    # <Wrong TX connector - not possible to route TX of the selecrted channel to the specified port
        2: 'ERROR_INCORRECT_RX_CONN',	    # <Wrong RX connector - not possible to route RX of the selecrted channel to the specified port
        3: 'ERROR_RXTX_SAME_CONN',	        # <Mode TXRX not allowed - when the same port is selected for RX and TX, it is not allowed to use mode RX & TX
        4: 'ERROR_CELL_WRONG_MODE',	        # <Wrong mode for cellular channel - Cellular FDD bands (1, 2, 3, and 7) are only allowed mode RX & TX, while TDD band 38 is allowed only RX or TX mode
        5: 'ERROR_CELL_TX_NOT_EQUAL_RX',	# <Cellular channels must be the same both for RX and TX
        6: 'ERROR_WRONG_CHANNEL_CODE'	    # <Requested channel code is wrong
    }
    return return_codes.get(code)

class rfe_boardstate(Structure):
    _fields_ = [
        ("channelIDRX", c_char),    # <RX channel ID (convenience constants defined in limeRFE.h).For example constant RFE_CID_HAM_0145 identifies 2m(144 - 146 MHz) HAM channel.
	    ("channelIDTX", c_char),    # <TX channel ID (convenience constants defined in limeRFE.h).For example constant RFE_CID_HAM_0145 identifies 2m(144 - 146 MHz) HAM channel. If - 1 then the same channel as for RX is used.
	    ("selPortRX",   c_char),    # <RX port (convenience constants defined in limeRFE.h).
	    ("selPortTX",   c_char),	# <TX port (convenience constants defined in limeRFE.h).
	    ("mode",        c_char),    # <Operation mode (defined in limeRFE.h). Not all modes all applicable to all configurations. HAM channels using same port for RX and TX are not allowed RFE_MODE_TXRX mode. Cellular FDD bands 1, 2, 3, and 7 are always in RFE_MODE_TXRX mode.Cellular TDD band 38 can not be in RFE_MODE_TXRX.
	    ("notchOnOff",  c_char),    # <Specifies whether the notch filter is applied or not (convenience constants defined in limeRFE.h).
	    ("attValue",    c_char),	# <Specifies the attenuation in the RX path. Attenuation [dB] = 2 * attenuation.
	    ("enableSWR",   c_char),	# <Enable SWR subsystem. (convenience constants defined in limeRFE.h).
	    ("sourceSWR",   c_char)	    # <SWR subsystem source. (convenience constants defined in limeRFE.h).
    ]

class board_info(Structure):
    _fields_ = [
        ('fw_ver',  c_char),        # Firmware version
        ('hw_ver',  c_char),        # Hardware version
        ('status1', c_char),        # Status (reserved for future use)
        ('status2', c_char)         # Status (reserved for future use)
    ]