# -*- coding: utf-8 -*-

"""Simple TCP server socket."""
import socket


HOST = '192.168.220.5'
PORT = 8888
MAX_CONN = 1
server = socket.socket(
    family=socket.AF_INET,
    type=socket.SOCK_DGRAM,
    proto=socket.IPPROTO_UDP,
)
server.bind((HOST, PORT))
data_recv, cl_addr = server.recvfrom(1024)
print(data_recv)
data_send = 'Your message has been received'.encode()
server.sendto(data_send, cl_addr)

server.close()
