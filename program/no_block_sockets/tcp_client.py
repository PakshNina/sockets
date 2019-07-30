# -*- coding: utf-8 -*-

"""Non blocking TCP client socket with timeout."""
import socket
import time


HOST = '192.168.220.5'
PORT = 8888
TIMEOUT = 5


def main():
    client = socket.socket()
    client.setblocking(False)
    client.settimeout(TIMEOUT)
    
    while True:
        connect(client)

def connect(client):
        client.connect((HOST, PORT))
        while True:
            message(client)


def message(client):
    try:
        data_recv = client.recv(1024)
        if data_recv:
            print(data_recv.decode())
        data_send = 'Message from client'
        client.send(data_send.encode())
    except socket.error as err:
        print(err)
        client.close()


if __name__ == '__main__':
    main()
