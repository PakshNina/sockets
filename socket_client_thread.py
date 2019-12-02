 
import socket
import time
import threading


class SocketClient(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.success = 0
        self.errors = 0
    
    def connect(self, number):
        client = socket.socket()
        client.connect((self.ip, self.port))
        outcome_message = 'Message from {0}'.format(number).encode()
        client.send(outcome_message)
        time.sleep(1)
        income_message = client.recv(1024)
        if income_message == outcome_message:
            print('{0}: success'.format(number))
            self.success += 1
        else:
            self.errors += 1
        client.close()

class MyThread(threading.Thread):
    def __init__(self, callback, number):
        threading.Thread.__init__(self)
        try:
            self.callback = callback
        except Exception as error:
            print(error)
        self.number = number

    def run(self):
        self.callback(self.number)

def create_client_threads(client):
    for number in range(100):
        my_thread = MyThread(client.connect, number)
        my_thread.start()


if __name__ == '__main__':
    client = SocketClient('127.0.0.1', 8888)
    create_client_threads(client)

