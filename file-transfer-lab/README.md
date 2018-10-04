In this repository you would fin the programs fileClient.py and fileServer.py along with the stammerProxy.py

To run the file transfer system you first run the stammerProxy to setup the proxy then you would run the fileServer to have the proxy
connect to the server.
Then before runnin the client you would have to change the port number of the client so it can connect to the proxy to do this you input:
`$ serverClient.py -s 127.0.0.1:50000`
then all the clients would connect to the proxy and would bve able to transfer any type of file to the server.
