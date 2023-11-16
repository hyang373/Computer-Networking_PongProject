# =================================================================================================
# Contributing Authors:     <Asmita Karki, Helen Yang>
# Email Addresses:          <aka271@uky.edu, hya230@uky.edu>
# Date:                     <11/16/2023 date last edited>
# Purpose:                  <This file implements the client side of the game. It sends the client's paddle's movement, 
#                           ball's location, and score to the server.>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================
# =================================================================================================
#Methods.  Please use the following template for all methods you write: 
# Author:      <Who wrote this method> 
# Purpose:      <What should this method do> 
# Pre:  <What preconditions does this method expect to be true? Ex. This method 
#expects the program to be in X state before being called> 
# Post:  <What postconditions are true after this method is called? Ex. This method 
#  changed global variable X to Y> 
# =================================================================================================
import pygame
import tkinter as tk
import sys
import socket
from assets.code.helperCode import *
import time
import json

# This is the main game loop.  
def playGame(screenWidth:int, screenHeight:int, playerPaddle:str, client:socket.socket) -> None:
    # Pygame inits
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()
 
    # Constants
    WHITE = (255,255,255)
    clock = pygame.time.Clock()
    scoreFont = pygame.font.Font("./assets/fonts/pong-score.ttf", 32)
    winFont = pygame.font.Font("./assets/fonts/visitor.ttf", 48)
    pointSound = pygame.mixer.Sound("./assets/sounds/point.wav")
    bounceSound = pygame.mixer.Sound("./assets/sounds/bounce.wav")
   
    # Display objects
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    winMessage = pygame.Rect(0,0,0,0)
    topWall = pygame.Rect(-10,0,screenWidth+20, 10)
    bottomWall = pygame.Rect(-10, screenHeight-10, screenWidth+20, 10)
    centerLine = []
 
    for i in range(0, screenHeight, 10):
        centerLine.append(pygame.Rect((screenWidth/2)-5,i,5,5))
    
    # Paddle properties and init
    paddleHeight = 50
    paddleWidth = 10
    paddleStartPosY = (screenHeight/2)-(paddleHeight/2)
    leftPaddle = Paddle(pygame.Rect(10,paddleStartPosY, paddleWidth, paddleHeight))
    rightPaddle = Paddle(pygame.Rect(screenWidth-20, paddleStartPosY, paddleWidth, paddleHeight))
    ball = Ball(pygame.Rect(screenWidth/2, screenHeight/2, 5, 5), -5, 0)
    
    if playerPaddle == "left":
        opponentPaddleObj = rightPaddle
        playerPaddleObj = leftPaddle
    else:
        opponentPaddleObj = leftPaddle
        playerPaddleObj = rightPaddle
    
    lScore = 0
    rScore = 0
    sync = 0
    game_over = False
 
    while True:
       
        # Wiping the screen
        screen.fill((0,0,0))
        
        # Getting keypress events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    playerPaddleObj.moving = "down"
                    # im adding this to send paddle position update to server
                    client.send(f"paddle {playerPaddle} down".encode())
                elif event.key == pygame.K_UP:
                    playerPaddleObj.moving = "up"
                    # im adding this to send paddle position update to server
                    client.send(f"paddle {playerPaddle} up".encode())      
            elif event.type == pygame.KEYUP:
                playerPaddleObj.moving = ""
        
        # =========================================================================================
        # sends an update to the server on the paddle's information
        try:
            clientGameData = {
                "playerPaddle" : [playerPaddleObj.rect[0], playerPaddleObj.rect[1]],
                "opponentPaddle" : [playerPaddleObj.rect[0], playerPaddleObj.rect[1]],
                "gameOver": game_over,
                "sync": sync
            }
            client.sendall(json.dumps(clientGameData).encode())
        except Exception as e:
            print(f"Error in syncing with other player | {e}")
        
        # =========================================================================================
        # Update the player paddle and opponent paddle's location on the screen
        for paddle in [playerPaddleObj, opponentPaddleObj]:
            if paddle.moving == "down":
                if paddle.rect.bottomleft[1] < screenHeight-10:
                    paddle.rect.y += paddle.speed
            elif paddle.moving == "up":
                if paddle.rect.topleft[1] > 10:
                    paddle.rect.y -= paddle.speed

        # If the game is over, display the win message
        if lScore > 4 or rScore > 4:
            game_over = True
            winText = "Player 1 Wins! " if lScore > 4 else "Player 2 Wins! "
            textSurface = winFont.render(winText, False, WHITE, (0,0,0))
            textRect = textSurface.get_rect()
            textRect.center = ((screenWidth/2), screenHeight/2)
            winMessage = screen.blit(textSurface, textRect)
        else:
            # ==== Ball Logic =====================================================================
            ball.updatePos()
            # If the ball makes it past the edge of the screen, update score, etc.
            if ball.rect.x > screenWidth:
                lScore += 1
                pointSound.play()
                ball.reset(nowGoing="left")
            elif ball.rect.x < 0:
                rScore += 1
                pointSound.play()
                ball.reset(nowGoing="right")
            # If the ball hits a paddle
            if ball.rect.colliderect(playerPaddleObj.rect):
                bounceSound.play()
                ball.hitPaddle(playerPaddleObj.rect.center[1])
            elif ball.rect.colliderect(opponentPaddleObj.rect):
                bounceSound.play()
                ball.hitPaddle(opponentPaddleObj.rect.center[1])
            # If the ball hits a wall
            if ball.rect.colliderect(topWall) or ball.rect.colliderect(bottomWall):
                bounceSound.play()
                ball.hitWall()
            pygame.draw.rect(screen, WHITE, ball)

            # ==== End Ball Logic =================================================================
        # Drawing the dotted line in the center
        for i in centerLine:
            pygame.draw.rect(screen, WHITE, i)
 
        # Drawing the player's new location
        for paddle in [playerPaddleObj, opponentPaddleObj]:
            pygame.draw.rect(screen, WHITE, paddle)
        pygame.draw.rect(screen, WHITE, topWall)
        pygame.draw.rect(screen, WHITE, bottomWall)
        scoreRect = updateScore(lScore, rScore, screen, WHITE, scoreFont)
        pygame.display.update()
        clock.tick(60)
        if(game_over == True):
            return
 
        # This number should be synchronized between you and your opponent.  
        sync += 1
 
        # =====# Receive and handle game state updates from the server
        data_info = client.recv(1024).decode()
        print(f"Received data: {data_info}")
        clientGameData.update(json.loads(data_info))
        opponentPaddleObj.rect.x = clientGameData["opponentPaddle"][0]
        opponentPaddleObj.rect.y = clientGameData["opponentPaddle"][1]
        game_over = clientGameData["gameOver"]
        sync = clientGameData["sync"]
        # =========================================================================================
 
def joinServer(ip:str, port:str, errorLabel:tk.Label, app:tk.Tk) -> None:
    # Purpose:      This method is fired when the join button is clicked
    # Arguments:
    # ip            A string holding the IP address of the server
    # port          A string holding the port the server is using
    # errorLabel    A tk label widget, modify it's text to display messages to the user (example below)
    # app           The tk window object, needed to kill the window
    # Create a socket and connect to the server
    # Get the required information from your server (screen width, height & player paddle, "left or "right)
    #--------------------------------------------------------------------
 
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, int(port)))  # Attempt to connect to the provided IP and port
        # If the connection was successful, proceed with the game
        errorLabel.config(text="Successfully connected to the server.\nWaiting for another player.")
        errorLabel.update()
        time.sleep(5)
        
        # Wait for the message from the server
        data = client.recv(1024).decode()
        # Split the received string into parts
        info_parts = data.split()
        if len(info_parts) >= 4 and info_parts[0] == "screen":
            screenWidth = int(info_parts[1])
            screenHeight = int(info_parts[2])
            playerPaddle = str(info_parts[3])
            errorLabel.config(text=f"You're on the {playerPaddle} side")
            errorLabel.update()
            time.sleep(2)
            # Now you can use screenWidth, screenHeight, and playerPaddle in your game logic
            app.withdraw()
            playGame(screenWidth, screenHeight, playerPaddle, client)
            time.sleep(5)
            app.quit()
    except ConnectionRefusedError:
        # Handle the case where the connection is refused (IP and port don't match)
        errorLabel.config(text="Connection failed. Check IP and Port.")
        errorLabel.update()
    except Exception as e:
        # Handle any other exceptions that might occur during the connection process
        errorLabel.config(text=f"Connection error: {str(e)}")
        errorLabel.update()
 
def startScreen():
    app = tk.Tk()
 
    app.title("Server Info")
    image = tk.PhotoImage(file="./assets/images/logo.png")
    titleLabel = tk.Label(image=image)
 
    titleLabel.grid(column=0, row=0, columnspan=2)
    ipLabel = tk.Label(text="Server IP:")
 
    ipLabel.grid(column=0, row=1, sticky="W", padx=8)
    ipEntry = tk.Entry(app)
 
    ipEntry.grid(column=1, row=1)
    portLabel = tk.Label(text="Server Port:")
 
    portLabel.grid(column=0, row=2, sticky="W", padx=8)
    portEntry = tk.Entry(app)
 
    portEntry.grid(column=1, row=2)
    errorLabel = tk.Label(text="")
 
    errorLabel.grid(column=0, row=4, columnspan=2)
    joinButton = tk.Button(text="Join", command=lambda: joinServer(ipEntry.get(), portEntry.get(), errorLabel, app))
 
    joinButton.grid(column=0, row=3, columnspan=2)
    app.mainloop()
 
if __name__ == "__main__":
    startScreen()
