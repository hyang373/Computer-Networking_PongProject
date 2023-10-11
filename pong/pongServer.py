# =================================================================================================
# Contributing Authors:	    <Anyone who touched the code>
# Email Addresses:          <Your uky.edu email addresses>
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

import socket
import threading

# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games

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
server.bind(('', 12345)) # binds server to a specific IP address and port

# start listening for connections 
server.listen(5)

# accept incoming connections
clientSocket, clientAddress = server.accept()

clientSocket.close()
server.close()


# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games
