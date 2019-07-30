# -*- coding: utf-8 -*-

"""Non blocking TCP server socket with timeout."""
import socket


HOST = '192.168.220.5'
PORT = 8888
MAX_CONN = 1
TIMEOUT = 5

def main():
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.setblocking(False)
    server.settimeout(TIMEOUT)
    server.listen(MAX_CONN)

    while True:
        connection(server)


def connection(server):
    try:
        client, cl_addr = server.accept()
        message(client)
    except socket.timeout:
        print('no connection')

def message(client):
    try:
        data_send = "You are connected"
        client.send(data_send.encode())
        data_recv = client.recv(1024)
        print(data_recv.decode())
    except socket.error as err:
        client.close()
        print(err)

def closing(server_socket):
    server.close()


if __name__ == '__main__':
    main()
