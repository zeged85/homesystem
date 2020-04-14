#!/usr/bin/env python

import socket
import select
import json
from msgFrame import * #address_to_bytes, bytes_to_address, createMessage, decode, encode, MESSAGESIZE

# db & dispatcher
class db:
    def __init__(self, server, username="admin", password=1234):
        self.server=server
        self.username=username
        self.password=password
        self.recvList = [self.server] # add sys.stdin for standalone
        #self.HEADERSIZE = 10
        print("DB init")



    def start(self):
        print(f"DB started")
        #server.sendall(bytes("hello server","utf-8"))
        try:
            while True:
                readyRecvList, readySendList, readyErrList = select.select(self.recvList, [], [])
                for fd in readyRecvList:
                    if fd == self.server:
                        self.server.settimeout(3)
                        try:
                            message = self.server.recv(2048)
                        except socket.timeout as err:
                            print("ERROR: DB: The recv() function timed out after 3 seconds! Try again.")
                        except Exception as e:
                            print("ERROR: DB: Something awful happened!")
                            print(type(e))    # the exception instance
                            print(e.args)     # arguments stored in .args
                            print(e)          # __str__ allows args to be printed directly,
                            raise
                        
                        if message == "" or message == b'':
                            print("none msg")
                            for fd in self.recvList:
                                fd.close()
                                exit(1)
                            break
                        else:
                            print (f"{message}\n")
                            self.handleMessage(message)
                            
                            #print(f"DB recieved from {ip}:{port} {jsonObj}")
                            #self.handleMessage(ip,port,jsonObj)


                        self.server.settimeout(None)
                        break

        except select.error as err:
            for fd in self.recvList:
                try:
                    tempRecvList, tempSendList, tempErrList = select.select([fd], [], [], 0)
                except select.error:
                    if fd == self.server:
                        fd.close()
                        exit(1)
                    else:
                        if fd in self.recvList:
                            self.recvList.remove(fd)
                            fd.close()

        except socket.error as err:
            print("ERROR: Cannot connect to chat server", err)
            print ("* Exiting... Goodbye! *")
            exit(1)

            if fd in self.recvList:
                fd.close()

        except KeyboardInterrupt:
            print("\nINFO: KeyboardInterrupt")
            print("* Closing all sockets and exiting chat server... Goodbye! *")
            self.server.close()
            exit(0)

    def handleMessage(self,message):
        b_address = message[:ADDRESSSIZE]
        ip, port = bytes_to_address(b_address)
        msg_len = int(message[ADDRESSSIZE:ADDRESSSIZE+MESSAGESIZE])
        print(f'message length {msg_len}')
        jsonObj = decode(message[ADDRESSSIZE + MESSAGESIZE:])
        print(f"DB says> got {jsonObj['type']} from {ip}:{port}")
        print(jsonObj)


        response = self.messageTypes["request"]["ping"](self)

        #if jsonObj['type']=="request":
        #    if jsonObj['message']=="ping":
        #        print("Pong!")
        #        dic = {
        #            "message":"pong",
        #            "type":"response"
        #        }
        #        toSend = json.dumps(dic)
        #        print(toSend)
        #        self.server.sendall(bytes(toSend, "utf-8"))

        self.server.sendall(b_address + response)

        

        


    def ping(self):
        msg = createMessage("pong","response","")
        b_msg = encode(msg)
        return b_msg


    
    requests = {
        "ping":ping
    }

    def pong(self):
        pass

    responses = {
        "pong":pong
    }


    messageTypes = {
        "request":requests,
        "response":responses
    }

    
  



