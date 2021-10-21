#!/usr/bin/env python3
import sys
import socket
import selectors
import types

#Register selector
sel = selectors.DefaultSelector()

#Data to send
messages = [b'Message 1 from client', b'Message 2 from client.']

#Start by initiating start_connections function
def start_connections(host, port, num_conns):
        server_addr = (host, port)
        for i in range(0, num_conns): #num_conns is read from the terminal - # of connections to create to the server
                connid = i + 1
                print('Starting connection', connid, 'to', server_addr)

                #Create unique socket and set blocking to false to accept traffic
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.setblocking(False)
                sock.connect_ex(server_addr) #Used instead of .connect() to not raise BlockingIOError exception. This just returns an error indicator - errno.EINPROGRESS (instead of raising exception)

                events = selectors.EVENT_READ | selectors.EVENT_WRITE #Return whether socket is ready for reading or writing after connection is completed

                #Create SimpleNamespace class to store data from socket
                data = types.SimpleNamespace(connid=connid,
                                                msg_total=sum(len(m) for m in messages), #total message length
                                                recv_total=0, #incrementor for data blocks received
                                                messages=list(messages), #Create list to copy data to send
                                                outb=b' ')

                sel.register(sock, events, data=data) #Register socket

#Service Connection Function
def service_connection(key, mask):

        sock = key.fileobj #Get socket info from key
        data = key.data #Get data from selector key

        if mask & selectors.EVENT_READ: #Check to see if the socket is ready to read data

                recv_data = sock.recv(1024) #Receive data

                if recv_data: #If data recevied
                        print('received', repr(recv_data), 'from connection', data.connid)
                        data.recv_total += 1

                if not recv_data or data.recv_total == data.msg_total: #If no more data to receieved (total message received or nothing present in register)
                        #Close connection
                        print('closing connection', data.connid)
                        sel.unregister(sock)
                        sock.close()

        if mask & selectors.EVENT_WRITE: #Check to see if the socket is ready to write data

                if not data.outb and data.messages: #If no data to write

                        data.outb = data.messages.pop(0) #Use .pop() to remove element from the index

                if data.outb: #if data to write

                        #Send data
                        print('sending', repr(data.outb), 'to connection', data.connid)
                        sent = sock.send(data.outb)
                        data.outb = data.outb[sent:]

#Check to see if all necessary arguments were specified by end-user
if len(sys.argv) != 4:
        print("usage:", sys.argv[0], "<host> <port> <num_connections>")
        sys.exit(1)

#Set variables to user specified values
host, port, num_conns = sys.argv[1:4]

#Start Connection
start_connections(host, int(port), int(num_conns))

try:
        #Main selector event loop
        while True:
                events = sel.select(timeout=1)
                if events:
                        for key, mask in events:
                                service_connection(key, mask)

                #Check for socket being monitored to continue
                if not sel.get_map():
                        break

except KeyboardInterrupt:
        print("Interrupted. Exiting.")

finally:
        sel.close()
