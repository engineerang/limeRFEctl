# Copyright 2023 Engineerang <engineerang@jpodtech.com>
# SPDX-License-Identifier: Apache-2.0

from flask import Flask, render_template, request
import json

from app.webstate import State
from app.limerfe import LimeRFE

webserver_state = State()
console = []
limerfe = LimeRFE()
        
app_limerfe = Flask(__name__)

@app_limerfe.route("/", methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        if request.form.get('action1') == 'Open':
            console.append('\n')
            result, messages = limerfe.limerfeConnect() # connect
            console.append(result)
            [console.append(x) for x in messages]

        elif request.form.get('action2') == 'Close':
            console.append('\n')
            result, messages = limerfe.closeRFE(limerfe.rfe, limerfe.lib) # close
            console.append(result)
            [console.append(x) for x in messages]

        elif request.form.get('action3') == 'To GUI':
            console.append('\n')
            console.append('LimeRFE configuration added to GUI:')
            result, messages = limerfe.getBoardState(limerfe.rfe, limerfe.lib) # get board state
            console.append(result)
            [console.append(x) for x in messages]
            
            # update GUI
            if result == 'SUCCESS':
                board_conf = [x.split()[1] for x in messages]
                webserver_state.updateDropdownSelected(webserver_state.checkChannel(board_conf[0]), board_conf[0], board_conf[2], board_conf[6], board_conf[5])

        elif request.form.get('action4') == 'Apply':
            # get setting from GUI
            chan = request.form.get('channel') 
            band = request.form.get('band')
            rx_port = request.form.get('port')
            attn = request.form.get('attn')
            notch = request.form.get('notch')
            if notch == None: notch = 0

            # Update GUI
            webserver_state.updateDropdownSelected(
                chan, 
                band,
                rx_port,
                attn,
                notch
                )
            
            # Configure LimeRFE
            result, messages = limerfe.configureBoard(
                limerfe.rfe, 
                limerfe.lib, 
                int(band), 
                int(band), 
                int(rx_port), 
                int(rx_port), 
                0, 
                int(notch), 
                int(attn), 
                0, 
                0
            )

            console.append('\n')
            console.append(result)
            [console.append(x) for x in messages]

        elif request.form.get('action5') == 'Get Info':
            console.append('\n')
            result, messages = limerfe.getBoardInfo(limerfe.rfe, limerfe.lib)
            console.append(result)
            [console.append(x) for x in messages]

        elif request.form.get('action6') == 'Reset':
            console.append('\n')
            result, messages = limerfe.resetBoard(limerfe.rfe, limerfe.lib) # reset board
            console.append(result)
            [console.append(x) for x in messages]

            if result == 'SUCCESS':               
                result, messages = limerfe.getBoardState(limerfe.rfe, limerfe.lib) # get board state
                console.append(result)
                console.append('LimeRFE configuration added to GUI:')
                [console.append(x) for x in messages]

                #Update GUI
                board_conf = [x.split()[1] for x in messages]
                webserver_state.updateDropdownSelected(webserver_state.checkChannel(board_conf[0]), board_conf[0], board_conf[2], board_conf[6], board_conf[5])

        elif request.form.get('action7') == 'Clear':
            console.clear()
        
        else:
            pass # unknown
    
    elif request.method == 'GET':
        return render_template(
            "index.html", 
            portList=webserver_state.getPortsList(), 
            attnList=webserver_state.getAttnList(),
            notch=webserver_state.getNotchList(),
            console=console
            )
    
    return render_template(
        "index.html",
        portList=webserver_state.getPortsList(), 
        attnList=webserver_state.getAttnList(),
        notch=webserver_state.getNotchList(),
        console=console
        )

@app_limerfe.route("/getcat", methods=["POST"])
def getcat():  

    data = dict(request.form)

    for i in webserver_state.getBandsList():
        if i['id'] == data['id']:
            return json.dumps(i['categories'])
