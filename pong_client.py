"""
Author: Danielle Lieberman
Program name: pong_client
Description: gets players, ball and score Coordinates and presents screen to player
Date: 03.05.26
"""

import sys
import pygame
import socket
import os
import pickle
import logging

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
DIVIDER_WIDTH = 4
DIVIDER_HEIGHT = 20
PLAYER_WIDTH  = 10
PLAYER_HEIGHT = 100
BALL_RADIUS = 15

PORT = 2009
LOG_DIR = "log"
LOG_FILE_CLIENT = os.path.join(LOG_DIR, "client.log")
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(filename=LOG_FILE_CLIENT,
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logging.info("Client program started")


# Create the client socket
pong_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
logging.info('Trying to connect to server 127.0.0.1: ' + str(PORT))
pong_client.connect(('127.0.0.1', PORT))
logging.info('Connected to server')

# Set a timeout so the loop does not get "stuck" waiting for data.
pong_client.settimeout(0.1)

# Get who am I (player 1 or player 2)
player_id = int(pong_client.recv(2048).decode())
logging.info("Received player id: " + str(player_id))

print("Player ID:", player_id)
print("Connected to server")



# Building the graphics
pygame.init()
logging.info("Pygame initialized")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pong Game')
game_font = pygame.font.SysFont("monospace", 35)

run = True

# Main loop
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # the X button was clicked
            logging.info("User clicked quit")
            run = False

    # Send input to the server
    msg = "NONE"

    # Read currently pressed keys
    # the variable "keys" will hold dictionary of bool for each key in the keyboard.
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        msg = "UP"
    if keys[pygame.K_DOWN]:
        msg = "DOWN"

    # Send the server my current direction
    try:
        pong_client.send(str.encode(msg))
    except Exception as e:
        logging.error("Failed sending message to server: " + str(e))
        break

    # Receive data from server.
    try:
        # First read the 4-byte header to know how big the incoming game state is.
        header = pong_client.recv(4)
        if not header:
            continue

        # Parse the header into int.
        data_size =   int.from_bytes(header, byteorder='big')

        # Then keep reading until we get the full payload
        data = b""
        while len(data) < data_size:
            packet = pong_client.recv(data_size - len(data))

            # Break in case of failure
            if not packet:
                break

            # Build the data from each packet.
            data += packet

        # Convert the raw data into python variable.
        game_state = pickle.loads(data)
        if game_state["game_over"]:
            logging.info("Game over received. Final score: player 1=" + str(game_state["p1_score"]) +
                         ", player 2=" + str(game_state["p2_score"]))
    except socket.timeout:
        # No data received this time, just skip to draw
        continue
    except Exception as e:
        logging.error("Failed receiving game state: " + str(e))
        continue

    # Draw

    screen.fill((0, 0, 0)) #rgb color (red, green, blue)

    # Vertical divider
    for y in range(0, SCREEN_HEIGHT, DIVIDER_HEIGHT * 2): # generate list of ys.

        # create rectangle
        pygame.draw.rect(screen, (255, 255, 255),  # color
                         (SCREEN_WIDTH / 2 - DIVIDER_WIDTH / 2,  # x position
                          y,  # y position
                          DIVIDER_WIDTH,  # the rectangle width
                          DIVIDER_HEIGHT))# the rectangle height

    # draw players

    # left player (player 1)
    pygame.draw.rect(screen, (255,255,255), (0, # x coordinate
                                          game_state["p1_y"],
                                          PLAYER_WIDTH, # width
                                          PLAYER_HEIGHT)) # height

    # right player (player 2)
    pygame.draw.rect(screen, (255,255,255), (SCREEN_WIDTH - PLAYER_WIDTH, # x coordinate
                                          game_state["p2_y"],
                                          PLAYER_WIDTH, # width
                                          PLAYER_HEIGHT)) # height
    # draw ball
    pygame.draw.ellipse(screen, (255, 255, 255), (game_state["ball_x"], # x coordinate
                                               game_state["ball_y"], # y coordinate
                                               BALL_RADIUS, # x radius
                                               BALL_RADIUS # y radius
                                               ))

    # draw score

    # generate the text graphics
    score_text = game_font.render(str(game_state["p1_score"]) + "   " +
                                  str(game_state["p2_score"]) , # text to show
                                  True , # antialias
                                  (255, 255, 255)) # color
    # draw the graphics
    screen.blit(score_text, (SCREEN_WIDTH // 2 - 52, 20))

    if game_state["game_over"]:
        game_over_text = game_font.render( "Game Over",
                                      True,  # antialias
                                      (255, 255, 255))  # color
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 95, SCREEN_HEIGHT // 2 - 80))

        winner = 1
        if(game_state["p2_score"] > game_state["p1_score"]):
            winner = 2
        winner_text = game_font.render("player " + str(winner) + " wins",
                                          True,  # antialias
                                          (255, 255, 255))  # color
        screen.blit(winner_text, (SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 55))
    # Update the screen
    pygame.display.update()

# Free resources
pygame.quit()
pong_client.close()
sys.exit()