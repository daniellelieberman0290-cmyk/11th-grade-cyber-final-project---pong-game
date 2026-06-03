"""
Author: Danielle Lieberman
Program name: pong_server
Description:creates players, ball and score Coordinates and sends them to clients
Date: 08.05.26
"""
import pickle
import socket
import threading
import time
import os
import logging

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
DIVIDER_WIDTH = 4
DIVIDER_HEIGHT = 20
PLAYER_WIDTH = 10
PLAYER_HEIGHT = 100
BALL_RADIUS = 15
BALL_SPEED = 1
PLAYER_SPEED = 1.5
MAX_SCORE = 5

SERVER_IP = '127.0.0.1'  # (localhost)
PORT = 2009

LOG_DIR = 'log'
LOG_FILE_SERVER = os.path.join(LOG_DIR, 'server.log')
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(filename=LOG_FILE_SERVER,
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logging.info('Server program started')

game_state = {"p1_y": 200,
              "p2_y": 200,
              "ball_x": 10,
              "ball_y": 100,
              "ball_speed_x": BALL_SPEED,
              "ball_speed_y": -BALL_SPEED,
              "p1_score": 0,
              "p2_score": 0,
              "game_over": False
              }

# Will contain the two clients connections
connections = []


def reset_ball_and_players():
    logging.info("Reset ball and players")
    # ball resetting
    game_state["ball_x"] = SCREEN_WIDTH // 2
    game_state["ball_y"] = SCREEN_HEIGHT // 2

    # Change direction
    game_state["ball_speed_x"] *= -1

    # players resetting
    game_state["p1_y"] = (SCREEN_HEIGHT / 2) - (PLAYER_HEIGHT / 2)
    game_state["p2_y"] = (SCREEN_HEIGHT / 2) - (PLAYER_HEIGHT / 2)


# player is 1 or 2
def move_player_up(player_id):
    logging.debug("Player " + str(player_id) + " moves up")
    if player_id == 1:

        if game_state["p1_y"] > 0:
            game_state["p1_y"] -= PLAYER_SPEED

    else:

        if game_state["p2_y"] > 0:
            game_state["p2_y"] -= PLAYER_SPEED


def move_player_down(player_id):
    logging.debug("Player " + str(player_id) + " moves down")
    if player_id == 1:

        if game_state["p1_y"] < SCREEN_HEIGHT - PLAYER_HEIGHT:
            game_state["p1_y"] += PLAYER_SPEED

    else:

        if game_state["p2_y"] < SCREEN_HEIGHT - PLAYER_HEIGHT:
            game_state["p2_y"] += PLAYER_SPEED


# Runs when a client connects.
def handle_client(conn, player_index):
    print("\nhandle_client")
    logging.info("Started handle_client for player " + str(player_index))
    global game_state
    # Tell the client if they are player 1 or 2
    print("\nplayer_index=" + str(player_index))

    conn.send(str.encode(str(player_index)))
    logging.info("Sent player id " + str(player_index) + " to client")

    # Receive the data from a client. (directions)
    while True:
        try:
            # Receive the data from the player
            data = conn.recv(2048).decode()

            # Abort if no data exists
            if not data:
                break

            # Update player position
            # data can be "UP" or DOWN"
            if data == "UP":
                move_player_up(player_index)
            if data == "DOWN":
                move_player_down(player_index)
        except Exception as e:
            logging.error("Error with player " + str(player_index) + ": " + str(e))
            break

    logging.info("Player " + str(player_index) + " disconnected")
    conn.close()


def game_logic():
    logging.info("Game logic thread started")
    global game_state

    while not game_state["game_over"]:
        # Move ball
        game_state["ball_x"] += game_state["ball_speed_x"]
        game_state["ball_y"] += game_state["ball_speed_y"]

        # Wall ball bounce (y-axis: top / bottom)
        if game_state["ball_y"] <= 0 or game_state["ball_y"] >= (SCREEN_HEIGHT - BALL_RADIUS):
            game_state["ball_speed_y"] *= -1
            logging.info("Ball bounced on top/bottom wall")

        # player 1 collision
        if (game_state["ball_x"] <= PLAYER_WIDTH and
                game_state["p1_y"] < game_state["ball_y"] < (game_state["p1_y"] + PLAYER_HEIGHT)):
            game_state["ball_speed_x"] *= -1
            logging.info("Ball hit player 1 paddle")

            # Prevent sticking
            game_state["ball_x"] = PLAYER_WIDTH

        # player 2 collision
        if (game_state["ball_x"] >= (SCREEN_WIDTH - PLAYER_WIDTH - BALL_RADIUS) and
                game_state["p2_y"] < game_state["ball_y"] < (game_state["p2_y"] + PLAYER_HEIGHT)):
            game_state["ball_speed_x"] *= -1
            logging.info("Ball hit player 2 paddle")

            # Prevent sticking
            game_state["ball_x"] = SCREEN_WIDTH - PLAYER_WIDTH - BALL_RADIUS

        # Goal left
        if game_state["ball_x"] < 0:
            game_state["p2_score"] += 1
            logging.info("Goal left: player 2 score is " + str(game_state["p2_score"]))

            reset_ball_and_players()

        # Goal right
        if game_state["ball_x"] > SCREEN_WIDTH:
            game_state["p1_score"] += 1
            logging.info("Goal right: player 1 score is " + str(game_state["p1_score"]))

            reset_ball_and_players()

        time.sleep(0.015)  # wait ~ 1 / 60 of a second.


pong_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pong_server.bind((SERVER_IP, PORT))
# start listen to incoming connection no more than 2 connections at one time
pong_server.listen(2)
logging.info("Server listening on " + str(SERVER_IP) + ": " + str(PORT))

for i in range(2):
    print("\naccepting " + str(i))
    # A client has been call the server first the first time.
    conn, addr = pong_server.accept()

    # Save the connection object for future communications.
    connections.append(conn)
    logging.info("Client connected from " + str(addr) + " as player " + str(i + 1))

    # Create a new thread which runs in parallel the "handle_clien" function with those arguments:
    # conn: the client connection
    # i   : player index (using the for loop index)
    thread = threading.Thread(target=handle_client, daemon=True, args=(conn, i + 1))

    # Start running the thread.
    thread.start()

    print("\nplayer " + str(i + 1) + " connected")
    logging.info("Player " + str(i + 1) + " connected")

# Start running the game.
threading.Thread(target=game_logic, daemon=True).start()

# while the game is running send each player the game state
#while ((game_state["p1_score"] < 5) and (game_state["p2_score"] < 5)):
while not game_state["game_over"]:
    game_state["game_over"] = not ((game_state["p1_score"] < MAX_SCORE) and (game_state["p2_score"] < MAX_SCORE))
    data = pickle.dumps(game_state)

    # Path the size of the data into 4 bytes.
    data_length = len(data).to_bytes(4, byteorder="big")

    for conn in connections:
        try:
            # Send size + data
            conn.sendall(data_length + data)
        except Exception as e:
            logging.error("Failed sending game state to client: " + str(e))
            pass
    time.sleep(0.015)

logging.info("Game over. Final score: player 1=" + str(game_state["p1_score"]) + ", player 2=" +
             str(game_state["p2_score"]))
input("\npress enter to quit")
