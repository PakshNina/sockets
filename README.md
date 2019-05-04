This repository include different Python utils with raw sockets

#######################
# syncSocketServer.py #
#######################

is a sync socket (TCP), that sends random data to the client every 1 second.
It only allows to connect one client at the time. 
After client disconects server still remains working and waiting for another client.
You can test the server with netcat util by typing following command in the command line:
> nc localhost 8888

It will return data in one line without breacking.
