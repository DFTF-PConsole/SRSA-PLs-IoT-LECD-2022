import sys
import socket
import os
from _thread import *

ThreadCount = 0
Client_number = 0

if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <host> <port>")
    sys.exit(1)
    
host, port = sys.argv[1], int(sys.argv[2])
ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))
    sys.exit(1)
    
print(f'Socket is listening in address {host} and port {port} ...')
ServerSocket.listen(5)

def multi_threaded_client(connection, cli_n):
    connection.send(str.encode('Server is working:'))
    while True:
        data = connection.recv(2048)
        response = 'Server message: I received ' + str(len(data.decode('utf-8'))) + ' chars: '+ data.decode('utf-8')
        if not data:
            break
        connection.sendall(str.encode(response))
    print('Bye bye Client ' + str(cli_n) + '!')
    connection.close()

try:
    while True:
        Client, address = ServerSocket.accept()
        Client_number +=1
        print('Connected to Client ' + str(Client_number) + ', calling from: ' + address[0] + ':' + str(address[1]))
        start_new_thread(multi_threaded_client, (Client, Client_number,))
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))
        
except KeyboardInterrupt:
    print("\nCaught keyboard interrupt, exiting")
finally:
    ServerSocket.close()
