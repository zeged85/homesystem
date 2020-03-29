#!/usr/bin/env python

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "10.0.0.41"
port = 10006


s.connect((host,port))

while True:
    cmd = input("client>")

    if cmd == 'quit':
        s.close()
        print(f"exiting")
        exit(0)

    msg = bytes(cmd, "utf-8")
    s.send(msg)
    #reply = s.recv(1024)
    #reply = reply.decode("utf-8")
    #print(f"server says: {reply}")
