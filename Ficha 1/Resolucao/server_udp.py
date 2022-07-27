import sys
import socket

ThreadCount = 0
Client_number = 0

if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <host> <port>")
    sys.exit(1)
    
host, port = sys.argv[1], int(sys.argv[2])
ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))
    sys.exit(1)
    
print(f'Socket is listening in address {host} and port {port} ...')

try:
    while True:
        data, addr = ServerSocket.recvfrom(1024)
        Client_number +=1
        print('Received message \"' + data.decode('utf-8') + '\" from Client ' + str(Client_number) + ', calling from: ' + addr[0] + ':' + str(addr[1]))
        
except KeyboardInterrupt:
    print("\nCaught keyboard interrupt, exiting")
finally:
    ServerSocket.close()
