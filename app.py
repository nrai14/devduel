import time
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from cards import cards_player_1, cards_player_2
import random

from lib.database_connection import get_flask_database_connection
# from lib.card import Card
from lib.card_repository import CardRepository

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
# define the countdown func.

def game():
    connection = get_flask_database_connection(app)

    # Generate decks for each player
    full_deck = list(range(1, 21))
    random.shuffle(full_deck)

    # full_deck = create_randomised_deck()
    player_1_deck = full_deck[0:10]
    player_2_deck = full_deck[10:20]
    black_hole = []
    print(f"PLAYER 1 DECK: {player_1_deck}")
    print(f"PLAYER 2 DECK: {player_2_deck}")

    repository = CardRepository(connection)

    # 5 minute timer starts
    duration = 300
    start_time = time.time()
        
    while len(player_1_deck) != 0 and len(player_2_deck) != 0:
        # Exit out of the game loop if play exceeds 5 minutes
        if time.time() - start_time > duration:
            print("Timeout")
            break

        # Select first card from players' decks
        card_1_id = player_1_deck[0]
        card_2_id = player_2_deck[0]
        print(f"PLAYER 1 CARD ID: {card_1_id}")
        print(f"PLAYER 2 CARD ID: {card_2_id}")
        
        player_1_card = repository.find_by_id(card_1_id)
        player_2_card = repository.find_by_id(card_2_id)


        # Player 1 selects an attribute
        # selected_attribute = request.args.get('selected_attribute')
        selected_attribute = "age"

        # Compare attributes from both cards
        player_1_value = repository.get_attribute_value(player_1_card, selected_attribute)
        player_2_value = repository.get_attribute_value(player_2_card, selected_attribute)
        print(f"AGE 1: {player_1_value}")
        print(f"AGE 2: {player_2_value}")

        if player_1_value > player_2_value:
            winner = "player 1"
            losing_card_id = card_2_id
        elif player_2_value > player_1_value:
            winner = "player 2"
            losing_card_id = card_1_id
        else:
            winner = "draw"

        if winner == "player 1":
            player_1_deck.append(losing_card_id)
            player_2_deck.remove(losing_card_id)
            player_1_deck = player_1_deck[1:]
            player_1_deck.append(card_1_id)
        elif winner == "player 2":
            player_2_deck.append(losing_card_id)
            player_1_deck.remove(losing_card_id)
            player_2_deck = player_2_deck[1:]
            player_2_deck.append(card_2_id)
        else:
            black_hole.append(card_1_id)
            black_hole.append(card_2_id)
            player_1_deck.remove(card_1_id)
            player_2_deck.remove(card_2_id)

        print("player 1 deck", player_1_deck)
        print("player 2 deck", player_2_deck)
        print("black hole", black_hole)
    
    return str(player_1_deck)

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
