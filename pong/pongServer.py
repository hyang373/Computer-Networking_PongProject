# =================================================================================================
# Contributing Authors:	    <Asmita Karki, Helen Yang>
# Email Addresses:          <aka271@uky.edu, hya230@uky.edu>
# Date:                     <09/27/2023 date last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

import socket
import threading

# Use this file to write your server logic


# server is a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # this is creating the server
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # working on local host need


# Create a function to handle each client
def handle_client(clientSocket):
    # Implement the game logic and communication here
    pass

#  IP = 128.163.35.46 
server.bind(('', 12345)) # binds server to a specific IP address and port

# start listening for connections 
server.listen(2)

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
