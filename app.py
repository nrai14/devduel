from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from cards import cards_player_1, cards_player_2
import random

load_dotenv()

app = Flask(__name__)
CORS(app, origins="http://localhost:5173")
socketio = SocketIO(app, cors_allowed_origins="http://localhost:5173")
clients = []


@app.route("/")
def index():
    return "Hello, World!"

'''
Card decks have 10 random cards each
Players receive 1 deck each
Top card on Player 1's deck is selected
5 minute timer starts
Player 1 selects an attribute for comparison
Highest attribute wins
Loser's card added to winner's deck
If draw, both cards added to black hole
Winner goes first next round
'''
@app.route("/gameplay", methods=["GET", "POST"])
def create_randomised_deck():
    all_card_ids = list(range(1, 21))
    random.shuffle(all_card_ids)
    print(all_card_ids)
    return all_card_ids

def game():
    # Generate decks for each player
    full_deck = create_randomised_deck()
    player_1_deck = full_deck[0:10]
    player_2_deck = full_deck[11:21]
    print(player_1_deck)
    print(player_2_deck)

    





@socketio.on("username")
def handle_username(username):
    if username not in clients:
        clients.append(username)
        if clients[0] == username:
            emit("data", cards_player_1, to=request.sid)
        elif clients[1] == username:
            emit("data", cards_player_2, to=request.sid)

    elif username in clients:
        if clients[0] == username:
            emit("data", cards_player_1, to=request.sid)
        elif clients[1] == username:
            emit("data", cards_player_2, to=request.sid)


@socketio.on("disconnect")
def handle_disconnect(username):
    if username in clients:
        clients.remove(username)


@socketio.on("message")
def handle_message(data):
    username = data.get("username")
    stat = data.get("stat")
    print(f"received message: {stat} from: {username}")
    emit("message", data)


if __name__ == "__main__":
    socketio.run(app)
