# Copyright 2023 Engineerang <engineerang@jpodtech.com>
# SPDX-License-Identifier: Apache-2.0

import app.limeRFE_H as LH

class State():

    def __init__(self):
        self.bandsList = [
            {
                'id': '0', 
                'categories': [{'id': 1, 'name': 'Wideband', 'selected': 'false'}, {'id': 2, 'name': 'HAM', 'selected': 'false'}, {'id': 3, 'name': 'Cellular', 'selected': 'false'}]
            },
            {
                'id': '1', 
                'categories': [{'id': LH.CID_WB_1000,'name': '1-1000MHz', 'selected': 'false'},{'id': LH.CID_WB_4000,'name': '1-4GHz', 'selected': 'false'}]
            },
            {
                'id': '2', 
                'categories': [
                    {'id': LH.CID_HAM_0030,'name': '<30Hz', 'selected': 'false'},
                    {'id': LH.CID_HAM_0070,'name': '50-70MHz', 'selected': 'false'},
                    {'id': LH.CID_HAM_0145,'name': '144-146MHz', 'selected': 'false'},
                    {'id': LH.CID_HAM_0220,'name': '220-225MHz', 'selected': 'false'},
                    {'id': LH.CID_HAM_0435,'name': '430-440MHz', 'selected': 'false'},
                    {'id': LH.CID_HAM_0920,'name': '902-928MHz', 'selected': 'false'},
                    {'id': LH.CID_HAM_1280,'name': '1240-1325MHz', 'selected': 'false'},
                    {'id': LH.CID_HAM_2400,'name': '2300-2450MHz', 'selected': 'false'},
                    {'id': LH.CID_HAM_3500,'name': '3300-3500MHz', 'selected': 'false'}
                    ]
            },
            {
                'id': '3', 
                'categories': [
                    {'id': LH.CID_CELL_BAND01,'name': 'Band1', 'selected': 'false'},
                    {'id': LH.CID_CELL_BAND02,'name': 'Band2', 'selected': 'false'},
                    {'id': LH.CID_CELL_BAND03,'name': 'Band3', 'selected': 'false'},
                    {'id': LH.CID_CELL_BAND07,'name': 'Band7', 'selected': 'false'},
                    {'id': LH.CID_CELL_BAND38,'name': 'Band38', 'selected': 'false'}
                    ]
            }
            ]
        self.portsList = [
            {'id': LH.PORT_1, 'name': 'Tx/RX(J3)', 'selected': 'false'}, 
            {'id': LH.PORT_2, 'name': 'Tx(J4)', 'selected': 'false'}, 
            {'id': LH.PORT_3, 'name': '30 TX/RX(J5)', 'selected': 'false'}
            ]
        self.attn = [
            {'id': 0, 'name': '0', 'selected': 'false'}, 
            {'id': 2, 'name': '2', 'selected': 'false'}, 
            {'id': 4, 'name': '4', 'selected': 'false'},
            {'id': 6, 'name': '6', 'selected': 'false'}, 
            {'id': 8, 'name': '8', 'selected': 'false'}, 
            {'id': 10, 'name': '10', 'selected': 'false'},
            {'id': 12, 'name': '12', 'selected': 'false'},
            {'id': 14, 'name': '14', 'selected': 'false'},  
        ]
        self.notch = [
            {'id': 1, 'name': 'notch', 'selected': 'false'}, 
        ]
    
    def checkChannel(self, band):
        for i in self.bandsList:
            if i['id'] == '0': pass
            else:
                for x in i['categories']:
                    if int(band) == x['id']:
                        return i['id']
    
    def setState(self, list_to_update, state):
        for i in list_to_update:
            if str(i['id']) == state:
                i['selected'] = 'true'
            else:
                i['selected'] = 'false'

    def updateDropdownSelected(self, channel, band, port, attn, notch):

        # Update channel and band selection
        for i in self.bandsList:
            if i['id'] == '0':
                self.setState(i['categories'], channel)
            else:
                self.setState(i['categories'], band)
                
        # update port selection
        self.setState(self.portsList, port)

        # update attn selection
        self.setState(self.attn, attn)

        # update notch filter selection
        self.setState(self.notch, notch)

        return f"{channel}, {band}, {port}, {attn}, {notch}"

    def getPortsList(self):
        return self.portsList

    def getBandsList(self):
        return self.bandsList
    
    def getAttnList(self):
        return self.attn
    
    def getNotchList(self):
        return self.notch