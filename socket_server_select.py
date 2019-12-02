# -*- coding: utf-8 -*-

"""TCP socket server with select."""

from abc import ABCMeta
import socket
import select
import queue
import time


class Singleton(ABCMeta):
    """Metaclass for singleton."""

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class SocketServerException(socket.error):
    """New class for socket.error."""

    def __init__(self, message, error):
        super().__init__(message, error)


class SocketSelectServer(object, metaclass=Singleton):
    def __init__(self, ip='127.0.0.1', port=8888, max_conn=5):
        """Init socket class."""
        self.ip = ip
        self.port = port
        self.max_conn = max_conn
        self.initialized = False

    def run(self):
        """Run socket server."""
        self.inputs = []
        self.outputs = []
        self.messages = {}
        while True:
            if self.initialized:
                sock_to_read, sock_to_write, sock_errors = select.select(
                    self.inputs,
                    self.outputs,
                    self.inputs,
                    0.1,
                )
                self._read_socket(sock_to_read)
                self._write_socket(sock_to_write)
                self._exception_socket(sock_errors)
                time.sleep(0.1)
            else:
                self._initialize()

    def _initialize(self):
        self.server_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
            socket.IPPROTO_TCP,
        )
        server_fd = self.server_socket.fileno()
        if server_fd < 0:
            self.initialized = False
            raise SocketServerException(
                'Error with creating sockets',
                'server_fd < 0',
            )
        self.server_socket.setblocking(0)
        self.server_socket.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1,
        )
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(self.max_conn)
        self.inputs.append(self.server_socket)
        self.initialized = True

    def _read_socket(self, sockets_to_read):
         for sock in sockets_to_read:
            if sock is self.server_socket:
                self._server_socket(sock)
            else:
                self._send_message(sock)

    def _server_socket(self, server_socket):
        client_socket, client_address = server_socket.accept()
        client_socket.setblocking(0)
        self.inputs.append(client_socket)
        self.messages[client_socket] = queue.Queue()

    def _send_message(self, sock):
        data_from_client = None
        try:
            data_from_client = sock.recv(1024)
            print(data_from_client.decode())
        except ConnectionResetError:
            self._delete_socket_connection(sock)
        if data_from_client:
            self.messages[sock].put(data_from_client)
            if sock not in self.outputs:
                self.outputs.append(sock)
        else:
            self._delete_socket_connection(sock)

    def _write_socket(self, socket_to_write):
        for sock in socket_to_write:
            echo_message = ''.encode()
            try:
                if sock.fileno() > 0:
                    echo_message = self.messages[sock].get_nowait()
                else:
                    self._delete_socket_connection(sock)
                    continue
            except queue.Empty :
                self.outputs.remove(sock)
            try:
                sock.send(echo_message)
            except ConnectionResetError:
                self._delete_socket_connection(sock)
        


    def _exception_socket(self, socket_errors):
        for sock in socket_errors:
            self._delete_socket_connection(self, sock)
            print('trying to delete server socket')
            if sock is self.server_socket:
                self.inputs = []
                self.outputs = []
                self.messages = {}
                self.initialized = False

    def _delete_socket_connection(self, sock):
        if sock in self.inputs:
            self.inputs.remove(sock)
        self.messages.pop(sock, None)
        if sock in self.outputs:
            self.outputs.remove(sock)
        sock.close()


if __name__ == '__main__':
    server = SocketSelectServer()
    server.run()
