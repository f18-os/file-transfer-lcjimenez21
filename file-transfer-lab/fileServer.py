#! /usr/bin/env python3

import sys,os

sys.path.append("../lib")       # for params

import re, socket, params

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

sock, addr = lsock.accept()
4
print("connection rec'd from", addr)

# newPath = r'/Users/Timmy/Desktop/OS/file-transfer-lcjimenez21/framed-echo/serverFiles'
newPath = (os.getcwd()+'/serverFiles')
print(newPath)
if not os.path.exists(newPath):
    os.makedirs(newPath)
    pass

from framedSock import framedSend, framedReceive

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
