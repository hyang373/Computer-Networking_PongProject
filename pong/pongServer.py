# =================================================================================================
# Contributing Authors:	    <Asmita Karki, Helen Yang>
# Email Addresses:          <aka271@uky.edu, hya230@uky.edu>
# Date:                     <09/27/2023 date last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

import socket
import threading
from queue import Queue

# Use this file to write your server logic

# server is a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # this is creating the server
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # working on local host need

# create a queue and set max size to 2
player_in_queue = Queue(maxsize=2)

# Function to handle each client
def handle_client(clientSocket, player_num):
    while True:
        # Implement game logic and communication here
        data = clientSocket.recv(1024)  # Receive data from the client
        if not data:
            break  # Connection closed by the client
        # Process the data and update game state
    clientSocket.close()

    
if (player_in_queue.full()):
    player1 = player_in_queue.get()
    player2 = player_in_queue.get()
    print(f"Player 1: {player1} Player 2: {player2}")

#  IP = 128.163.35.46 
server.bind(('10.113.33.101', 12345)) # binds server to a specific IP address and port

# start listening for connections 
server.listen(10)

while True:
    clientSocket, clientAddress = server.accept()
    # Start a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(clientSocket,))
    client_thread.start()
    
# accept incoming connections


clientSocket.close()
server.close()


# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games
