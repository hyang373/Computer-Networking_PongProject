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

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = " "  # Replace with your server's IP address
server_port = 12345  # Choose a port
server_socket.bind((server_ip, server_port))
server_socket.listen(2)  # Accept up to 2 clients
print("Server is waiting for connection")

