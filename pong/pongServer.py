import socket
import threading
 
# Globol Variables
clientSocket0: socket
clientSocket1: socket
SIZE: int
 
def client0Thread():
    print("Client1 Thread Function Entered")
    try:
        while True:
            # get data from clients
            data = clientSocket0.recv(SIZE)
            if data == b"finished":
                return
            clientSocket1.send(data)
    except:
        return
 
def client1Thread():
    print("Client2 Thread Function Entered")
    try:
        while True:
            data = clientSocket1.recv(SIZE)
            if data == b"finished":
                return
            clientSocket0.send(data)
    except:
        return
 
def startServer():

    # local ip address & port
    localIP = "10.113.33.191"
    localPort = 12345
    
    # connect server to ip and port number
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((localIP, localPort))
    
    while True: 

        server.listen(2)    # number of clients waiting in queue for for "accept"
                            # If queue is full then client can't connect.
        
        print("Use this IP in clients: " + localIP)
        
        SIZE = 1024
        
        # accept the two client's socket and address in queue
        clientSocket0, clientAddress0 = server.accept()
        clientSocket1, clientAddress1 = server.accept()
        
        print(f"Client1: {clientSocket0} \nClient2: {clientSocket1}" )
        
        # Send player information to clients
        data = "screen 640 480 player1 left player2 right"
        data1 = "screen 640 480 player1 right player2 left"
        print(data)
        clientSocket0.send(data.encode("utf-8")[:1024])
        clientSocket1.send(data1.encode("utf-8")[:1024])

        thread0 = threading.Thread(target=client0Thread)
        thread1 = threading.Thread(target=client1Thread)
        
        thread0.start()
        thread1.start()
        print("threads started")

        thread0.join()
        thread1.join()
        print("threads joined")
        
        clientSocket0.close()
        clientSocket1.close()

if __name__ == "__main__":

    startServer()
