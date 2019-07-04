""" Non block socket with select """

import socket
import select
import queue

IP = '127.0.0.1'
PORT = 8888
MAXCONN = 5

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind((IP, PORT))
server_sock.listen(MAXCONN)

inputs = [server_sock]
outputs, exceptions = [], []

while inputs:
    read_sockets, _, _ = select.select(inputs, outputs, exceptions)
    try:
        for sock in read_sockets:
            if sock == server_sock:
                conn, client_addr = sock.accept()
                conn.setblocking(0)
                inputs.append(conn)
            else:
                data = sock.recv(1024)
                if data:
                    print(data.decode())
                else:
                    inputs.remove(sock)
                    sock.close()
    except socket.error as err:
        print(err)
        break

for sock in inputs:
    sock.close()
    inputs = []