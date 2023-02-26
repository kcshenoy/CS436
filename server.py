import sys
from socket import *

def create_socket(sock_type, n_port):
    serverSocket = socket(AF_INET,sock_type)
    serverSocket.bind(('',n_port))
    return serverSocket

def tcp_neg(serverSocket, req_code, r_port):

    serverSocket.listen(1)
    print('THE TCP SERVER IS READY TO RECEIVE')

    while True:
        connectionSocket, addr = serverSocket.accept()
        code = int(connectionSocket.recv(1024).decode())
        print('CLIENT REQUEST CODE: ' + str(code))

        if code == req_code:
            print('REQUEST CODE VERIFIED')
            udp_socket = create_socket(SOCK_DGRAM, r_port)
            r_port = str(udp_socket.getsockname()[1])
            print(r_port)
            connectionSocket.send(r_port.encode())
            return udp_socket

        else:
            print('ERROR: REQUEST CODE INVALID')
            connectionSocket.send("-1".encode())
            connectionSocket.close()
    
def udp_reverse(sock):
    print('THE UDP SERVER IS READY TO RECEIVE')
    message, clientAddress = sock.recvfrom(1024)
    modifiedMessage = message.decode()[::-1]

    print('MESSAGE REVERSED')
    sock.sendto(modifiedMessage.encode(), clientAddress)
    

def main():
    try:
        n_port = int(sys.argv[1])
        req_code = int(sys.argv[2])
    except ValueError:
        print("BOTH REQUEST CODE AND PORT NUMBER MUST BE INTEGERS. RETRY")
        sys.exit(-1)
    except IndexError:
        print("MISSING PARAMETER (REQUEST CODE, PORT). RETRY")
        sys.exit(-1)
    serverSocket = create_socket(SOCK_STREAM, n_port)

    while True:
        sock = tcp_neg(serverSocket, req_code, n_port)
        udp_reverse(sock)

if __name__ == "__main__":
    main()

# n_port = int(sys.argv[1])
# req_code = int(sys.argv[2])
# r_port = '2704'

# # Init TCP connection:
# serverSocket = socket(AF_INET,SOCK_STREAM)
# serverSocket.bind(('',n_port))
# serverSocket.listen(1)
# print ('The TCP server is ready to receive')

# while True:
#     connectionSocket, addr = serverSocket.accept()
#     code = int(connectionSocket.recv(1024).decode())
#     print(req_code==code)
#     if code != req_code:
#         connectionSocket.close()
#     else 


# print('success')
# print(addr)
# connectionSocket.send(r_port.encode())
# connectionSocket.close()

# # Init UDP connection:
# serverSocket = socket(AF_INET, SOCK_DGRAM)
# serverSocket.bind(('', int(r_port)))
# print ('The UDP server is ready to receive')

# message, clientAddress = serverSocket.recvfrom(1024)
# modifiedMessage = message.decode()[::-1]
# serverSocket.sendto(modifiedMessage.encode(), clientAddress)

# print('hey')
# serverSocket.bind(('',n_port))
# serverSocket.listen(1)



    
