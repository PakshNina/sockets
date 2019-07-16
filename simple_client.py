import socket
import sys
from PyCRC.CRCCCITT import CRCCCITT as crc

class SimpleClient(object):
    """
    Simple TCP socket client
    """
    IP = '127.0.0.1'
    PORT = 8888
    SAMPLE_DATA = 'SAMPLE DATA'

    def __init__(self, **kwargs):
        self.IP = kwargs['ip'] if 'ip' in kwargs else SimpleClient.IP
        self.port = kwargs['port'] if 'port' in kwargs else SimpleClient.PORT

        try:
            self.sock = socket.socket()
            self.sock.connect((self.IP, self.PORT))
        except socket.error as err:
            raise socket.error('Client problem', err)
    
    def send(self, message):
        try:
            data = message
            crc_sum = crc().calculate(message)
            data += '\n{}\n\n'.format(str(crc_sum))
            self.sock.send(data.encode())
        except socket.error as err:
            raise socket.error('Problem with sending', err)

    def recv(self):
        try:
            data = self.sock.recv(1024)
            data = data.decode()
            if data:
                if '\n\n' in data:
                    return data.strip('\n\n')
            else:
                print('error')
        except socket.error as err:
            raise('Error with sending', err)
   
    def close(self):
        self.sock.close()


if __name__ == '__main__':
    client = SimpleClient(port=8888)
    client.send('test')
    data = client.recv()
    print(data)