import socket
import time

#Variable Declaration
server = "127.0.0.1"
port = 4445

#Functions
def send(msg):
        s.send(msg.encode("UTF-8"))

def getInstruction():
        while True:
                msg = s.recv(4096)
                cmd = msg.decode("UTF-8")

                if (cmd) == "test":
                        try:
                                send("[OK]")
                        except:
                                print("error on send")
                                pass

#Connection
s = socket.socket((socket.AF_INET), socket.SOCK_STREAM)
host = socket.gethostname()
connected = False

while connected == False:
        try:
                s.connect((host, port))
                connection = True
        except:
                time.sleep(30)
print("connected")
getInstructions()
