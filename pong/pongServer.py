import socket
import threading
import json

# Globol Variables
clientSocket0: socket
clientSocket1: socket
SIZE: int
 
def client_thread(client_socket, target_socket):
    try:
        while True:
            try:
                data = client_socket.recv(SIZE)
                print(f"Received data: {data}")
                client_data = json.loads(data.decode("utf-8"))
                target_socket.send(json.dumps(client_data).encode("utf-8"))
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")

    except Exception as e:
        print(f"Client thread error: {e}")
    finally:
        print("Closing client socket.")
        client_socket.close()

 
def startServer():
    try:
        # local ip address & port
        localIP = "10.113.33.191"
        localPort = 12345
   
        # connect server to ip and port number
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((localIP, localPort))
        server.listen(2)    # number of clients waiting in queue for for "accept"                
        # If queue is full then client can't connect.
   
        print("Use this IP in clients: " + localIP)
   
        #SIZE = 1024
        
        # accept the two client's socket and address in queue
        clientSocket0, clientAddress0 = server.accept()
        clientSocket1, clientAddress1 = server.accept()
   
        # Send player information to clients
        data = "screen 640 480 left"
        data1 = "screen 640 480 right"
        clientSocket0.send(data.encode("utf-8")[:1024])
        clientSocket1.send(data1.encode("utf-8")[:1024])
   

        thread0 = threading.Thread(target=client_thread, args=(clientSocket0, clientSocket1))
        thread1 = threading.Thread(target=client_thread, args=(clientSocket1, clientSocket0))
       
   
        thread0.start()
        thread1.start()
   
        thread0.join()
        thread1.join()
   
        clientSocket0.close()
        clientSocket1.close()
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        server.close()
 
if __name__ == "__main__":
    SIZE = 1024
    startServer()
