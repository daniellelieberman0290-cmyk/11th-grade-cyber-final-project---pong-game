"""
Author: Danielle Lieberman
Program name: pong_client
Description: gets players, ball and score coordinations and presents screen to player
Date: 03.05.26
"""

#import  socket
#import os
#import logging
import sys
import pygame
from pygame.examples.aliens import Player

#PORT = 2009
#LOG_DIR = "log"
#LOG_FILE_CLIENT = os.path.join(LOG_DIR, "client.log")


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
DIVIDER_WIDTH = 4
DIVIDER_HEIGHT = 20
PLAYER_WIDTH  = 10
PLAYER_HEIGHT = 100
BALL_RADIUS = 15

#5 next lines need to be in server
p1_y = 200
ball_x = 10
ball_y = 100
ball_vx = .4
ball_vy = -.4

pygame.init()

# setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pong Game')
game_font = pygame.font.SysFont("monospace", 35)

# TODO: create client (socket)
#def main():
#    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    try:
#        server_socket.connect(('127.0.0.1', PORT))
#        logging.info(f"Connected to server at 127.0.0.1:{PORT}")
#        print("Connected to server")

run = True
while run:
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # the X button was clicked
            run = False
    # Input

    # Read currently pressed keys
    # the variable "keys" will hold dictionary of bool for each key in the keyboard.
    keys = pygame.key.get_pressed()

#   command = ""

#    if keys[pygame.K_UP]:
#        command = "UP"
#    if keys[pygame.K_DOWN]:
#        command = "DOWN"
#
#   if command != "":
#        client.send(command.encode())

#    data = client.recv(1024).decode()

#    p1, p2, ball_x, ball_y = data.split(",")

#    p1_y = int(p1)
#    p2_y = int(p2)
#    ball_x = int(ball_x)
#    ball_y = int(ball_y)

#can delete two next if's?
    if keys[pygame.K_UP]:
        p1_y -= .5
    if keys[pygame.K_DOWN]:
        p1_y += .5

#two next if's need to be in server
    #if p1_y < 0:
    #    p1_y = 0

    #if p1_y > SCREEN_HEIGHT - PLAYER_HEIGHT:
    #    p1_y = SCREEN_HEIGHT - PLAYER_HEIGHT

#    if (ball_x <= PLAYER_WIDTH and
#            p1_y < ball_y < p1_y + PLAYER_HEIGHT):
#        ball_vx *= -1

#    if (ball_x >= SCREEN_WIDTH - PLAYER_WIDTH - BALL_RADIUS and
#            p2_y < ball_y < p2_y + PLAYER_HEIGHT):
#        ball_vx *= -1

    # Move ball (needs to be in server)
    ball_x += ball_vx
    ball_y += ball_vy

    # Wall bounce (y axis: top / bottom)
    if ball_y <=0 or ball_y >= (SCREEN_HEIGHT - BALL_RADIUS):
        ball_vy *= -1

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

    # left player.
    pygame.draw.rect(screen, (255,255,255), (0, # x coordinate
                                          #(SCREEN_HEIGHT / 2) - (PLAYER_HEIGHT / 2), # 2 coordinate
                                          p1_y,
                                          PLAYER_WIDTH, # width
                                          PLAYER_HEIGHT)) # height
    pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH - PLAYER_WIDTH, (SCREEN_HEIGHT / 2) - (PLAYER_HEIGHT / 2), PLAYER_WIDTH, PLAYER_HEIGHT))

    # draw ball
    pygame.draw.ellipse(screen, (255, 255, 255), (ball_x, # x coordinate
                                               ball_y, # y coordinate
                                               BALL_RADIUS, # x radius
                                               BALL_RADIUS # y radius
                                               ))

    # draw score

    # generate the text graphics
    score_text = game_font.render("0   0", # text to show
                                  True , # antialias
                                  (255, 255, 255)) # color
    # draw the graphics
    screen.blit(score_text, (SCREEN_WIDTH // 2 - 52, 20))

#after a win returning the ball to the middle and making it start to the oposit direction
#    ball_vx = -ball_vx
#    ball_y = SCREEN_HEIGHT // 2

    pygame.display.update()

#if __name__ == '__main__':
#    # create folder if it doesn't exist
#    if not os.path.isdir(LOG_DIR):
#        os.makedirs(LOG_DIR)

    # Configure logging: save all messages to a file
#    logging.basicConfig(
#        level=logging.INFO,
#        format='%(asctime)s - %(levelname)s - %(message)s',
#        filename=LOG_FILE_CLIENT,
#        filemode="a"
#    )
#    main()

# Free resources
pygame.quit()
sys.exit()