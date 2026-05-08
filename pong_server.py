import socket
import threading
import time

#TODO: logging

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
DIVIDER_WIDTH = 4
DIVIDER_HEIGHT = 20
PLAYER_WIDTH  = 10
PLAYER_HEIGHT = 100
BALL_RADIUS = 15

server_ip = '127.0.0.1' # (localhost)
port = 5555

game_state = {"p1_y":200,
              "p2_y":200,
              "ball_x":10,
              "ball_y":100,
              "ball_speed_x":.4,
              "ball_speed_y":-.4,
              "p1_score":0,
              "p2_score":0
              }
connections = []

def handle_client(conn, player_index):
    global game_state

    while True:
        try:
            # Receive the data from the player
            data = conn.recv(2048).decode()

            # TODO update player possition

            # Abort if no data exists
            if not data: break

        except Exception as e:
            break
    conn.close()

def game_logic():
    global game_state

    # Move ball
    game_state["ball_x"] += game_state["ball_speed_x"]
    game_state["ball_y"] += game_state["ball_speed_y"]

    # Wall bounce (y-axis: top / bottom)
    if game_state["ball_y"] <= 0 or game_state["ball_y"] >= (SCREEN_HEIGHT - BALL_RADIUS):
        game_state["ball_speed_y"] *= -1

    # player 1 collision
    if game_state["ball_x"] < PLAYER_WIDTH and game_state["ball_y"] < game_state["ball_y"] and game_state["ball_y"] > (game_state["ball_y"] - PLAYER_HEIGHT):
        game_state["ball_speed_x"] *= -1
