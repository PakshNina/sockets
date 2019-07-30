import socket 


def main():
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('192.168.220.5', 8181))
    server_socket.setblocking(False)
    server_socket.settimeout(5)
    server_socket.listen()

    while True:
        connection(server_socket)


def connection(server_socket):
    try:
        client_socket, addr = server_socket.accept()
        message(client_socket)
    except socket.timeout:
        print('no connection')

def message(client_socket):
    data = client_socket.recv(1024)
    if data:
        print(data.decode())
        reply = "I've received your data {0}".format(data.decode())
        client_socket.send(reply.encode())
    else:
        client_socket.close()

def closing(server_socket):
    server_socket.close()


if __name__ == '__main__':
    main()
