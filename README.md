# CS436 Coding Assignment 1: Instructions
## Krishnacharan Shenoy, ID: 20845406
This file contains instructions on how to run a 2-stage TCP and UDP socket program in a client-server env. The first stage involves negotiation between the client and server through a TCP connection, where the client sends a `req_code`, and if it matches the `req_code` on the server side, the client receives `r_port` where the server is listening using UDP for the input string to be reversed, and closes their connection. The client creates a UDP socket to the server in `r_port` and sends `msg` to be reversed.

## Instructions:
To run our scripts directly, we need to allow executable permissions, starting with the server:
```
chmod +x ./server.sh
./server.sh <n_port> <req_code>
```
where:
- `n_port`: integer representing negotiation port where TCP server is listening
- `req_code`: integer representing the request code for the server. If it matches the client's `req_code`, the server sends the UDP `r_port` the server will accept the `msg` on.

After the server has started, switch to your client machine allow executable permissions for the client script as well:
```
chmod +x ./client.sh
./client.sh <addr> <n_port> <req_code> <msg>
```
where:
- `addr`: string representing of the server for the client to contact
- `n_port`: integer representing negotiation port where TCP server is listening
- `req_code`: integer representing the request code the client sends, and is checked with the server's `req_code`. If they match the client receives the UDP port the server will accept the `msg` on.
- `msg`: message to be reversed

### Program Tested on the following:
ubuntu2004-004 and ubuntu2004-002 UWaterloo CS Undergraduate Linux Servers

