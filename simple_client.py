import socket
import sys

IP = '127.0.0.1'
PORT = 8888

try:
    sock = socket.socket()
    sock.connect((IP, PORT))
except socket.error as err:
    print(err)

while True:
    try:
        data = input()
        if data == 'exit':
            break
        else:
            sock.send(data.encode())
    except socket.error as err:
        print(err)
        break
sock.close()
