# -*- coding: utf-8 -*-

"""Simple TCP server socket."""
import socket


HOST = '192.168.220.5'
PORT = 8888
MAX_CONN = 1
server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)
server.bind((HOST, PORT))
server.listen(MAX_CONN)
client, cl_addr = server.accept()
data_recv = client.recv(1024)
print(data_recv.decode())
data_send = "I've got your message"
client.send(data_send.encode())

client.close()
server.close()
