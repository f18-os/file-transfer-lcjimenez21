#! /usr/bin/env python3
import sys

sys.path.append("../lib")       # for params

import os, socket, params


switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

newPath = (os.getcwd()+'/serverFiles')
if not os.path.exists(newPath):
    os.makedirs(newPath)
    pass

while True:
    sock, addr = lsock.accept()

    from framedSock import framedSend, framedReceive

    if not os.fork():
        print("new child process handling connection from", addr)
        while True:
            print("Receiving payload...")
            payload = framedReceive(sock)
            if not payload:
                print("Received: ", payload)#debug tool
                sys.exit(0)
            else:
                fileName = payload.decode()
                payload = framedReceive(sock)
                path = (newPath +'/'+ fileName)
                # print(path) debug tool
                out_file = open(path, "wb+") #[w]rite as [b]inary
                out_file.write(payload)
                out_file.close()
                framedSend(sock, payload, 1)

        print("Done!")
