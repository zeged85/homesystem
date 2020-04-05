#!/usr/bin/env python
import json
import socket
import sys
ADDRESSSIZE = 6
MESSAGESIZE = 10


def decode(data):
    #print (f"{data}\n")
    #msg_len = int(data[ADDRESSSIZE : ADDRESSSIZE + MESSAGESIZE])
    #print(f'message length {msg_len}')
    #print(data[HEADERSIZE:])
    jsonObj = json.loads(data)
    #print(jsonObj)
    return jsonObj


def encode(message):
    toSend = json.dumps(message)
    #print(toSend)
    rep = f'{len(toSend):<{MESSAGESIZE}}' + toSend
    return bytes(rep, "utf-8")

 
def createMessage(message, mType, mArgs):
    pyDic = {
        "message":message,
        "type":mType,
        "args":mArgs
        }
    return pyDic

def address_to_bytes(address):
    ip = address[0]
    port = address[1]
    b_ip = socket.inet_aton(ip)
    b_port = int(port).to_bytes(2,byteorder=sys.byteorder)
    return b_ip, b_port

def bytes_to_address(b_address):
    b_ip = b_address[:4]
    b_port = b_address[4:]
    ip = socket.inet_ntoa(b_ip)
    port = int.from_bytes(b_port, byteorder=sys.byteorder)
    return ip, port
                      
