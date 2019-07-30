# -*- coding: utf-8 -*-

r"""Non block socket with select.

The end of line - is \n\n simbol.
"""

import socket
import select
from PyCRC.CRCCCITT import CRCCCITT as CRC
import time


class ServerTCPSocket(object):
    """Server socket with select."""

    ip = '127.0.0.1'
    port = 8888
    max_conn = 3
    END = '\n\n'

    def __init__(self, **kwargs):
        """Initialyzing server."""
        self.ip = kwargs['ip'] if 'ip' in kwargs else ServerTCPSocket.ip
        self.port = (
            kwargs['port'] if 'port' in kwargs else
            ServerTCPSocket.port
            )
        self.max_conn = (
            kwargs['max_conn'] if 'max_conn' in kwargs else
            ServerTCPSocket.max_conn
            )
        self.client_activity = {}
        self.send_message = {}

    def start(self):
        """Start server."""
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.ip, self.port))
        self.server.listen(self.max_conn)

        self.inputs = [self.server]
        self.outputs = []

        while self.inputs:
            self.read_sockets, self.write_sockets, _ = select.select(
                self.inputs, self.outputs, [],
                )
            try:
                self._read_sock()
                self._write_sock()

            except socket.error as err:
                raise socket.error('Error', err)

    def _read_sock(self):
        for sock in self.read_sockets:
            client_addr = ''
            if sock == self.server:
                self.client_conn, self.client_addr = sock.accept()
                self.client_conn.setblocking(0)
                self.inputs.append(self.client_conn)
            else:
                client_message = sock.recv(1024)
                client_message = client_message.decode()
                if client_message and ServerTCPSocket.END in client_message:
                    client_message = client_message.replace(ServerTCPSocket.END, '')
                    self.client_activity[sock] = time.time()
                    crc_check = self._check_sum(client_message)
                    self.send_message[sock] = self._answer(crc_check)
                    if sock not in self.outputs:
                        self.outputs.append(sock)
                else:
                    self._clear_sockets(sock, self.client_addr)

    def _check_sum(self, client_message):
        check_data = client_message.rsplit('\n', 1)
        check_sum = CRC().calculate(check_data[0])
        return int(check_data[1]) == check_sum

    def _answer(self, crc_check):
        if crc_check:
            return 'Ok' + ServerTCPSocket.END
        else:
            return 'Error' + ServerTCPSocket.END

    def _clear_sockets(self, sock, addr):
        self.inputs.remove(sock)
        if sock in self.send_message:
            self.send_message.pop(sock, None)
        if sock in self.client_activity:
            self.client_activity.pop(sock, None)
        if sock in self.outputs:
            self.outputs.remove(sock)
        sock.close()
        print('Client {0} disconnected.'.format(addr[0]))

    def _write_sock(self):
        for sock in self.write_sockets:
            if sock in self.send_message:
                sock.send(self.send_message[sock].encode())
                self.send_message.pop(sock, None)


if __name__ == '__main__':
    server = ServerTCPSocket(max_conn=5)
    server.start()
