  GNU nano 5.1                                                                                                                                                           serv.py                                                                                                                                                                     
import socket
import os

#Variable Declaration
port=4445

def clear():
        os.system('cls' if os.name=='nt' else 'clear')


#Begin Listening for Connection
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
serversocket.bind((host,port))
serversocket.listen(1)

clear()

print("Basic Remote Administration Tool")
clientsocket, addr = serversocket.accept()
print("Connection from: " + str(addr))

while True:
        cmd = input("$: ")

        if cmd == "help":
                print("Available Commands:    ")
                print("    test : Test server connection to client")

        elif cmd == "exit":
                clientsocket.shutdown(socket.SHUT_RDWR)
                clientsocket.close()

        else:
                ecmd = cmd.encode("UTF-8")
                clientsocket.send(ecmd)

                ercv = clientsocket.recv(4096)
                print(ercv.decode("UTF-8"))
