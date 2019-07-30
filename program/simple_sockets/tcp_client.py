# -*- coding: utf-8 -*-

"""Simple TCP client socket."""
import socket


HOST = '192.168.220.5'
PORT = 8888
client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)
client.connect((HOST, PORT))
data_send = 'Message from client'
client.send(data_send.encode())
data_recv = client.recv(1024)
print(data_recv.decode())
client.close()
