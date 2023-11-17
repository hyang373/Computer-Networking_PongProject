# =================================================================================================
# Contributing Authors:     Asmita Karki, Helen Yang
# Email Addresses:          aka271@uky.edu, hya230@uky.edu
# Date:                     11/17/2023 date last edited
# Purpose:                  The server is responsible for facilitating a 2 player game by handling their communication.
#                           It uses socket programming and threading to allow the players to simultaneously play each other.
#                           The server relays location of the other player's paddle, ball's position, and current score.
# =================================================================================================
import socket
import threading
import json
import threading
 
# Global Variables
clientSocket0: socket
clientSocket1: socket
SIZE: int
lock = threading.Lock() # create lock object

def client_thread(client_socket:socket, target_socket:socket) -> None:
    # =================================================================================================
    # Author:      Asmita Karki & Helen Yang
    # Purpose:     This handles communication with the client
    # Pre:         client_socket and target_socket should be valid sockets.
    #              it should be able to receive data from client_socket.
    # Post:        It actively receives data from client_socket.
    #              It decodes the JSON data and sends it to target_socket (other player).
    # =================================================================================================
    try:
        while True:
            try:
                # receive data from the client
                data = client_socket.recv(SIZE)
                if not data:
                    break
                print(f"Received data: {data}")
                with lock:
                    # decode JSON data and send it to the other client
                    client_data = json.loads(data.decode("utf-8"))
                    target_socket.sendall(json.dumps(client_data).encode("utf-8"))
                    # automatically released because im using "with lock"
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
 
    except Exception as e:
        print(f"Client thread error: {e}")
    finally:
        print("Closing client socket.")
        client_socket.close()
 
def startServer():
    # =================================================================================================
    # Author:      Asmita Karki & Helen Yang
    # Purpose:     This function sets up the server
    # Pre:         The localIP address and localPort should be available for use. 
    # Post:        The server is able to facilitate communication between the clients.
    #              The client sockets are accepted.
    #              Threads start to handle communication.
    # =================================================================================================

    try:
        # local ip address & port
        localIP = "10.113.33.101" 
        localPort = 12345
   
        # connect server to ip and port number
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((localIP, localPort))
        server.listen(2)    # number of clients waiting in queue for "accept"                
        # If queue is full then client can't connect.
   
        print("Use this IP in clients: " + localIP)
          
        # accept the two client's socket and address in queue
        with lock: 
            clientSocket0, clientAddress0 = server.accept()
            clientSocket1, clientAddress1 = server.accept()
   
        # Send player information to clients
        data = "screen 640 480 left"
        data1 = "screen 640 480 right"
        with lock:
            clientSocket0.send(data.encode("utf-8")[:1024])
            clientSocket1.send(data1.encode("utf-8")[:1024])

        # start thread for the 2 clients
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
