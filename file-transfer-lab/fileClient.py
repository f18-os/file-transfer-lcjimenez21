#! /usr/bin/env python3

# Echo client program
import socket, sys, re

sys.path.append("../lib")       # for params
import params

from framedSock import framedSend, framedReceive


switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)


print("Name of file to transfer:")
args = input()
if ".txt" in args:
    header = str.encode(args)# Get file name
    file = open(args, "r")
    data = file.read().replace('\n', ' ')
    data = data.encode()
    print("Sending %s to Server..." % args)
    framedSend(s, header, 1) #Name of file
    framedSend(s, data, 1) #Content from file
    print("Received:", framedReceive(s, debug))#debug tool
else:
    byte_args = str.encode(args)# Get file name
    file = open(args, "rb")
    print("sending %s" % args)
    framedSend(s, byte_args, 1) #Name of file
    framedSend(s, file.read(), 1) #Content from file
    print("received:", framedReceive(s, debug))
    pass
