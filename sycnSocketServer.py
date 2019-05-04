import socket
import random
import time

def server():
        hServer =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        hServer.bind(('localhost', 8888))
        print('Server stated')
        hServer.listen()
        while True:
                try:
                        print('Waiting for the client to connect')
                        hClient, addr = hServer.accept()
                        print('Connection from', addr)
                        client(hClient)
                except Exception as err:
                        print('Sorry, as error has occured:', err)

def client(hClient):
        while True:
                try:
                        data = str(random.random())
                        hClient.send(data.encode())
                        ##timeout 
                        time.sleep(1)
                except Exception as err:
                        print(err)
                        break

        hClient.close()

server()
