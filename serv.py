#!/usr/bin/env python3
import selectors
import socket

host="0.0.0.0"
port=65432

#Register new socket connection. Create new socket object and register with selector.
def accept_wrapper(sock):
        conn, addr = sock.accept() #Accept sock connection - ready to read
        print('Connection accepted from', addr)

        conn.setblocking(False) #Accept data from socket connection

        data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'') #Object to hold data and socket info

        events = selectors.EVENT_READ | selectors.EVENT_WRITE #Set events for keeping track of when client connections is ready for reading and writing

        sel.register(conn, events, data=data) #Pass mask, socket, and data to selector

#Service already registered connection using key (namedtuple returned from selector) and mask (contains events that are ready)
def service_connection(key, mask):

        sock = key.fileobj #key.fileobj is the socket object
        data = key.data #key.data is the data object

        if mask & selectors.EVENT_READ: #Use socket and events to determine if data is ready to be received

                recv_data = sock.recv(1024) #Receive data from socket

                if recv_data: #If any data was received
                        data.outb += recv_data #add data to store

                else: #Close connection if determine if the client has closed their socket
                        print('Closing connection to', data.addr)
                        sel.unregister(sock)
                        sock.close()

        if mask & selectors.EVENT_WRITE: #If ready to write data

                if data.outb: #If data is available to write
                        print('echoing', repr(data.outb), 'to', data.addr)
                        sent = sock.send(data.outb)
                        data.outb = data.outb[sent:] #Send data using sock.send()



sel = selectors.DefaultSelector() #Register selector

#Open listening socket
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print('listening on', (host, port))

lsock.setblocking(False) #Accept data from socket connection

sel.register(lsock, selectors.EVENT_READ, data=None) #Register socket to be monitored with sel.select(). Use data variable to store what's been sent/received

#Main Event Loop
while True:
        events = sel.select(timeout=None) #Block call until a monitored socket file object is ready

        #For each key/mask socket pair the selector selects from it's register
        for key, mask in events:

                if key.data is None: #If key.data is None, then we know it's a socket that's been accepted that needs to be serviced

                        accept_wrapper(key.fileobj) #Send to wrapper function to get new socket and register it with the selector

                else:

                        service_connection(key, mask) #Service connection using key and socket mask information already gathered
