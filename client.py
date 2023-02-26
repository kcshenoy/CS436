import sys
from socket import *

def tcp_neg(addr, n_port, req_code):
    try:
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((addr,n_port))
        clientSocket.send(req_code.encode())

        r_port = int(clientSocket.recv(1024))

        if r_port < 0:
            print("INVALID REQUEST CODE")
            sys.exit(-1)

        clientSocket.close()
        return r_port
    
    except error as e:
        print('CONNECTION ERROR: ' + str(e.args))
        sys.exit(-1)

def udp_send_msg(addr, r_port, msg):
    print("UDP TRANSACTION")
    serverPort = r_port
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    message = msg
    print("UDP MESSAGE SENT TO BE REVERSED")
    clientSocket.sendto(message.encode(), (addr, int(serverPort)))
    modifiedMessage = clientSocket.recv(1024).decode()
    clientSocket.close()
    return modifiedMessage

def main():
    try:
        address = str(sys.argv[1])
        n_port = int(sys.argv[2])
        req_code = sys.argv[3]
        msg = str(" ".join(sys.argv[4:]))
    except IndexError:
        print("MISSING PARAMETER (SERVER ADDRESS, PORT, REQUEST CODE, MESSAGE). RETRY")
        sys.exit(-1)
    except ValueError:
        print("ADDRESS, MESSAGE MUST BE STRINGS."
                "PORT, REQUEST CODE MUST BE INTEGERS. RETRY")
        sys.exit(-1)
    
    print(msg)
    r_port = tcp_neg(address, n_port, req_code)
    message = udp_send_msg(address, r_port, msg)
    print("CLIENT MESSAGE REVERSED: " + str(message))

if __name__=='__main__':
    main()
