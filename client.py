import sys
from socket import *

'''
tcp_neg(addr, n_port, req_code) sends req_code to the server to be checked with 
its req_code, where:

    addr: IP address/hostname of socket, type str
    n_port: port where TCP server is hosted, type str
    req_code: code to be tested for match, type int

req_code is sent to the server, and the response is recorded as r_port. If r_port is 
negative/invalid, then we exit the script, else we close the connection and return 
our r_port which we use to create the UDP socket for our transaction phase. If our 
connection is invalid due to a wrong n_port or addr, we show a connection error and 
exit the script.
'''
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


'''
udp_send_msg(addr, r_port, msg) returns the original message modified by the server,
where:

    addr: IP address/hostname of socket, type str
    r_port: port where UDP server is hosted, type int
    msg: message to be reversed, type str

Create the socket, and then send the message over to the server for it to be reversed.
We then receive it and return the modified message.
'''
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


'''
main() is responsible for running the script, where:

    address: IP address/hostname of socket, type str
    n_port: port where initial TCP negotiation takes place, type int
    req_code: request code to be checked with client request code, type int
    msg: message to be reversed, type str

All 4 parameters are read from input and checked for validity and existence. if both 
exceptions are not triggered, we create the server socket for the TCP negotiation phase. 
From the negotiation phase, we use the returned port to create the UDP socket to initiate 
the transaction phase. 
'''
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
