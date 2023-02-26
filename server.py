import sys
from socket import *

'''
create_socket(sock_type, n_port) creates a new socket, given parameters sock_type
and n_port, where:

    sock_type: type of socket, eg. SOCK_DGRAM (UDP), type string
    n_port: port where server is hosted, type int

Returns the socket binded to n_port of type Socket
'''
def create_socket(sock_type, n_port):
    serverSocket = socket(AF_INET,sock_type)
    serverSocket.bind(('',n_port))
    return serverSocket


'''
tcp_neg(serverSocket, req_code, r_port) takes parameters serverSocket, 
req_code, and r_port, and returns a UDP socket if negotiation with
client is succesful, where:

    serverSocket: where TCP server socket is listening for client,
                type Socket
    req_code: request code which is to be checked by the request code
            sent by client, type int
    r_port: port where TCP server is listening for client req_code
            type int

While running, if the client request code matches our req_code, the server
returns the port where our UDP server will be waiting for the message to 
be reversed. If request codes do not match, we send an error code/invalid
port number to the client and close the connection socket.
'''
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
    

'''
udp_reverse(sock) decodes the client message, reverses the string, and sends
it back to the client, where:
    sock: UDP server socket which communicates with client, type Socket
'''
def udp_reverse(sock):
    print('THE UDP SERVER IS READY TO RECEIVE')
    message, clientAddress = sock.recvfrom(1024)
    modifiedMessage = message.decode()[::-1]

    print('MESSAGE REVERSED')
    sock.sendto(modifiedMessage.encode(), clientAddress)
    

'''
main() is responsible for running the script, where:

    n_port: port where initial TCP negotiation takes place, type int
    req_code: request code to be checked with client request code, type int

Both n_port and req_code are read from input and checked for validity and
existence. if both exceptions are not triggered, we create the welcoming socket
for the TCP negotiation phase. From the negotiation phase, we use the returned
UDP socket to initiate the transaction phase. 
'''
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
