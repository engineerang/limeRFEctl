# Copyright 2023 Engineerang <engineerang@jpodtech.com>
# SPDX-License-Identifier: Apache-2.0

from ctypes import cdll, byref, c_int, c_void_p, c_char_p, POINTER
import app.limeRFE_H as LH
import struct
import serial.tools.list_ports
import glob

class LimeRFE():

    def __init__(self):
        self.rfe = None
        self.lib = None
    
    # Load libLimeSuite shared object
    def loadLibLimeSuite(self, lib_limesuite_path):
        try:
            return cdll.LoadLibrary(lib_limesuite_path)
        except Exception as e:
            raise SystemExit(e)

    def openRFE(self, comport):
        try:
            # self.rfe = c_void_p()
            return self.lib.RFE_Open(c_char_p(comport.encode('utf-8')), None)
        except Exception as e:
            raise SystemExit(e)
        
    def limerfeConnect(self, port=None, lib=None):

        messages = []
        # find limerfe device com port
        if not port:
            comports = []
            for com in serial.tools.list_ports.comports():
                if com.manufacturer == 'FTDI' and com.vid == 1027 and com.pid == 24577:
                    messages.append("Suspected LimeRFE device found.")
                    messages.append(com.hwid)
                    messages.append(com.device)
                    comports.append(com.device)
            if not comports:
                messages.append("No serial devices found.")
                return "Error", messages
            elif len(comports) > 1:
                messages.append("Multiple devices found.")
                for com in comports:
                    messages.append(com)
                messages.append('Please specify a com port.')
                return "Error", messages
            else:
                comport = com.device
        else:
            comport = port
        
        # find libLimeSuite shared object
        if not lib:
            lib_paths = glob.glob('/usr/lib/*-linux-gnu/libLimeSuite.so')
            if not lib_paths:
                messages.append("No libLimeSuite.so found. Please install 'liblimesuite-dev'.")
                return "Error", messages
            if len(lib_paths) > 1:
                messages.append("Multiple libraries found.")
                for lib_limesuite_path in lib_paths:
                    messages.appends(lib_limesuite_path)
                messages.append('Please specify a libLimeSuite.so to use.')
            else: 
                messages.append(lib_paths[0])
                self.lib = self.loadLibLimeSuite(lib_paths[0])
        else:
            self.lib = self.loadLibLimeSuite(lib)
        
        # Open serial port to limerfe
        self.rfe = self.openRFE( comport)
        if (self.rfe == 0):
                return "Error initializing serial port", messages
        else:
            messages.append("Port opened")
            return "SUCCESS", messages

    # GetBoardInfo
    def getBoardInfo(self, rfe, libLimeSuite):
        
        if rfe is None or libLimeSuite is None:
            return 'ERROR_COMM', ['Connect to LimeRFE!']
        
        messages = []
        info = LH.board_info() # info = (c_ubyte*4)() is also valid
        result = libLimeSuite.RFE_GetInfo(rfe, byref(info))
        if result == 0:
            messages.append("LimeRFE Firmware version: %d" % struct.unpack('<B', getattr(info, info._fields_[0][0]))[0])
            messages.append("LimeRFE Hardware version: 0x%x" % struct.unpack('<B', getattr(info, info._fields_[1][0]))[0])
            return LH.checkReturnCodes(result), messages
        else:
            return LH.checkReturnCodes(result), messages

    # GetBoardState
    def getBoardState(self,rfe, libLimeSuite):
        
        if rfe is None or libLimeSuite is None:
            return 'ERROR_COMM', ['Connect to LimeRFE!']

        messages = []
        state = LH.rfe_boardstate()
        result = libLimeSuite.RFE_GetState(rfe, byref(state)) 
        
        if result == 0:
            for field in state._fields_:
                messages.append(f"{field[0]}: {struct.unpack('<B', getattr(state, field[0]))[0]}")
            return LH.checkReturnCodes(result), messages 
        else:
            return LH.checkReturnCodes(result), messages

    # RFEConfigure
    def configureBoard(self, rfe, libLimeSuite, ch_id_rx, ch_id_tx, rx_port, tx_port, mode, notch, attn, enable_swr, source_swr):

        if rfe is None or libLimeSuite is None:
            return 'ERROR_COMM', ['Connect to LimeRFE!']
        
        messages = []

        result = libLimeSuite.RFE_Configure(
            rfe, 
            c_int(ch_id_rx),    # channelIDRX
            c_int(ch_id_tx),    # channelIDTX
            c_int(rx_port),     # selPortRX
            c_int(tx_port),     # selPortTX
            c_int(mode),        # mode
            c_int(notch),       # notchOnOff
            c_int(attn),        # attenuation
            c_int(enable_swr),  # enableSWR          
            c_int(source_swr)   # sourceSWR
        )

        if result == 0:
            messages.append('LimeRFE configured with: ')
            messages.append(f"({ch_id_rx}, {ch_id_tx}, {rx_port}, {tx_port}, {mode}, {notch}, {attn}, {enable_swr}, {source_swr})")

        return LH.checkReturnCodes(result), messages
    
    # RFEReset
    def resetBoard(self, rfe, libLimeSuite):

        if rfe is None or libLimeSuite is None:
            return 'ERROR_COMM', ['Connect to LimeRFE!']

        messages = []

        result = libLimeSuite.RFE_Reset(rfe)
        
        if result == 0:
            messages.append('LimeRFE configuration reset')

        return LH.checkReturnCodes(result), messages
    
    # RFEClose
    def closeRFE(self, rfe, libLimeSuite):

        if rfe is None or libLimeSuite is None:
            return 'ERROR_COMM', ['Connect to LimeRFE!']

        messages = []

        result = libLimeSuite.RFE_Close(rfe)

        if result == 0:
            messages.append('Closed')
            self.rfe = None
            self.lib = None

        return LH.checkReturnCodes(result), messages
        
    # TODO RFELoadConfig
    def loadRFEConfig(rfe, libLimeSuite):
        raise SystemExit(NotImplementedError("loadRFEConfig Not implemented"))
