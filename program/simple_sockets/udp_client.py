# -*- coding: utf-8 -*-

"""Simple TCP client socket."""
import socket


HOST = '192.168.220.5'
PORT = 8888
server_adrr = (HOST, PORT)
client = socket.socket(
    family=socket.AF_INET,
    type=socket.SOCK_DGRAM,
    proto=socket.IPPROTO_UDP,
)
client.connect((HOST, PORT))
data_send = 'Message from client'
client.sendto(data_send.encode(), server_adrr)
data_recv, cl_addr = client.recvfrom(1024)
print(data_recv.decode(), 'from address:', cl_addr[0], cl_addr[1])
client.close()
