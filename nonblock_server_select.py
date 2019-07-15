""" Non block socket with select """

import socket
import select
import re


class ServerTCPSocket(object):
    def __init__(self, **kwargs):
        self.__ip = kwargs['ip'] if 'ip' in kwargs else '127.0.0.1'
        self.__port = kwargs['port'] if 'port' in kwargs else 8888
        self.__max_conn = kwargs['max_conn'] if 'max_conn' in kwargs else 3
    
    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.__ip, self.__port))
        self.server.listen(self.__max_conn)

        inputs = [self.server]
        outputs = []
        exceptions = []

        while inputs:
            read_sockets, werite_sockets, exception_sockets = select.select(inputs, outputs, exceptions)

            try:
                for sock in read_sockets:
                    if sock == self.server:
                        client_conn, client_addr = sock.accept()
                        client_conn.setblocking(0)
                        inputs.append(client_conn)
                    else:
                        data = sock.recv(1024)
                        data = data.decode()
                        print(data)
                        if data:
                            if re.search('id:\d{8}', data):
                                print('ok')
                        else:
                            inputs.remove(sock)
                            sock.close()
            except:
                inputs.remove(sock)
                


if __name__ == '__main__':
    server = ServerTCPSocket(max_conn=5)
    server.start()

# server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_sock.bind((IP, PORT))
# server_sock.listen(MAXCONN)

# inputs = [server_sock]
# outputs, exceptions = [], []

# while inputs:
#     read_sockets, _, _ = select.select(inputs, outputs, exceptions)
#     try:
#         for sock in read_sockets:
#             if sock == server_sock:
#                 conn, client_addr = sock.accept()
#                 conn.setblocking(0)
#                 inputs.append(conn)
#             else:
#                 data = sock.recv(1024)
#                 if data:
#                     print(data.decode())
#                 else:
#                     inputs.remove(sock)
#                     sock.close()
#     except socket.error as err:
#         print('Client {0} has disconnect with error: {1}'.format(client_addr(1), err))
#         inputs.remove(sock)
#         sock.close()
#         pass

# for sock in inputs:
#     sock.close()
#     inputs = []