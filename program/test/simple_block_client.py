import socket


client_socket = socket.socket()
client_socket.setblocking(False)
client_socket.settimeout(5)
client_socket.connect(('192.168.220.5', 8181))
client_socket.send('My message'.encode())
data = client_socket.recv(1024)
print(data.decode())
client_socket.close()
