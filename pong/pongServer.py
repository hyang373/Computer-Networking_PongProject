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

# server is a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # this is creating the server 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # working on local host need
# Bind the server to a specific IP address and port
server.bind(('10.113.33.101', 12345))
# Start listening for connections
server.listen(2) # listen for 2 clients


# create a queue and set max size to 2
player_in_queue = Queue(maxsize=2)

# from chatgpt
# Initialize a dictionary to store game state for both players
game_state_dict = {
    "player1": None,
    "player2": None
}

# Function to retrieve the data from the other player
def get_data_from_other_player(player_num):
    # If player_num is 1, get data from player2; if player_num is 2, get data from player1
    other_player_num = 2 if player_num == 1 else 1
    return game_state_dict[f"player{other_player_num}"]

# Function to update the game state for a player
def update_game_state(player_num, game_state):
    game_state_dict[f"player{player_num}"] = game_state

# Function to handle each client
def handle_client(clientSocket, player_num):
    try:
       #clientSocket, clientAddress = server.accept()
        # Determine player roles ("left" or "right")
        player1_role = "left" if player_num == 1 else "right"
        player2_role = "left" if player_num == 2 else "right"
        
        # Send the playerPaddle information to the client
        clientSocket.send(player1_role.encode() if player_num == 1 else player2_role.encode())
        while True:
            data = clientSocket.recv(1024) # Receive data from the client
            # Decode the received data to a string
            data_str = data.decode()
            if not data:
                break  # Connection closed by the client
            # Process the data and update game state
            update_game_state(player_num, data_str)
            # Determine the other player
            other_player = 2 if player_num == 1 else 1
            # Get data from the other player
            other_player_data = get_data_from_other_player(other_player)
            # Send the game state information back to both players
            clientSocket.send(other_player_data.encode('utf-8')) # string
    except Exception as e:
        print(f"Client {player_num} disconnected: {e}")
    finally:
        clientSocket.close()
        
while True:
    clientSocket, _ = server.accept()
    if player_in_queue.full():
        player1 = player_in_queue.get()
        player2 = clientSocket
        # Determine screen dimensions
        screenWidth = 800  # Set your desired screen width
        screenHeight = 600  # Set your desired screen height
        # Determine player paddles
        player1_paddle = "left"
        player2_paddle = "right"
        # Send acknowledgment message with game info to both clients
        ack_message = f"ACK screen {screenWidth} {screenHeight} player1 {player1_paddle} player2 {player2_paddle}"
        clientSocket.send(ack_message.encode('utf-8'))

        print(f"Player 1: {player1} Player 2: {player2}")
        clientSocket.send("start".encode('utf-8'))
        
        # Start the game loop with both player
        client_thread = threading.Thread(target=handle_client, args=(player1, player2))
        client_thread.start()
        
        # Continue to wait for a second player
        #player_in_queue.put(clientSocket)
    else:
        player_in_queue.put(clientSocket) 
