"""
Author: Danielle Lieberman
Program name: pong_client
Description: gets players, ball and score coordinations and presents screen to player
Date: 03.05.26
"""

import sys

import pygame
# from pygame.examples.aliens import Player

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
DIVIDER_WIDTH = 4
DIVIDER_HEIGHT = 20
PLAYER_WIDTH  = 10
PLAYER_HEIGHT = 100
BALL_RADIUS = 15

p1_y = 200
ball_x = 10
ball_y = 100
ball_vx = .4
ball_vy = -.4

pygame.init()

# setup
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pong Game')
game_font = pygame.font.SysFont("monospace", 35)

# TODO: create client (socket)

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

    if keys[pygame.K_UP]:
        p1_y -= .5
    if keys[pygame.K_DOWN]:
        p1_y += .5

    # Move ball
    ball_x += ball_vx
    ball_y += ball_vy

    # Wall bounce (y axis: top / bottom)
    if ball_y <=0 or ball_y >= (SCREEN_HEIGHT - BALL_RADIUS):
        ball_vy *= -1

    # Draw
    win.fill((0, 0, 0)) #rgb color (red, green, blue)

    # Vertical divider
    for y in range(0, SCREEN_HEIGHT, DIVIDER_HEIGHT * 2): # generate list of ys.

        # create rectangle
        pygame.draw.rect(win, (255, 255, 255),  # color
                         (SCREEN_WIDTH / 2 - DIVIDER_WIDTH / 2,  # x position
                          y,  # y position
                          DIVIDER_WIDTH,  # the rectangle width
                          DIVIDER_HEIGHT))# the rectangle height

    # draw players

    # left player.
    pygame.draw.rect(win, (255,255,255), (0, # x coordinate
                                          #(SCREEN_HEIGHT / 2) - (PLAYER_HEIGHT / 2), # 2 coordinate
                                          p1_y,
                                          PLAYER_WIDTH, # width
                                          PLAYER_HEIGHT)) # height
    pygame.draw.rect(win, (255, 255, 255), (SCREEN_WIDTH - PLAYER_WIDTH, (SCREEN_HEIGHT / 2) - (PLAYER_HEIGHT / 2), PLAYER_WIDTH, PLAYER_HEIGHT))

    # draw ball
    pygame.draw.ellipse(win, (255, 255, 255), (ball_x, # x coordinate
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
    win.blit(score_text, (SCREEN_WIDTH // 2 - 52, 20))

    pygame.display.update()

# Free resources
pygame.quit()
sys.exit()