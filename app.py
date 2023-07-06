from flask import Flask, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import random
from helpers.adjust_deck import transfer_card, remove_both
from lib.database_connection import get_flask_database_connection
from lib.card_repository import CardRepository


app = Flask(__name__)
CORS(app, origins="http://localhost:5173")
socketio = SocketIO(app, cors_allowed_origins="http://localhost:5173")

leading_player = None
client_usernames = []
client_decks = {}
client_sids = {}
player_1_deck = []
player_2_deck = []
black_hole = []


def initialize_decks():
    global player_1_deck, player_2_deck
    with app.app_context():
        connection = get_flask_database_connection(app)
        card_repository = CardRepository(connection)
        all_cards = card_repository.all()
        random.shuffle(all_cards)
        player_1_deck = all_cards[0:10]
        player_2_deck = all_cards[11:20]


@socketio.on("username")
def handle_username(username):
    global leading_player
    if username not in client_usernames:
        client_usernames.append(username)
        client_sids[username] = request.sid
        if client_usernames[0] == username:
            leading_player = username
            client_decks[username] = player_1_deck
            emit("data", player_1_deck[0], to=request.sid)
        elif client_usernames[1] == username:
            client_decks[username] = player_2_deck
            client_sids[username] = request.sid
            emit("data", player_2_deck[0], to=request.sid)

    elif username in client_usernames:
        if client_usernames[0] == username:
            client_sids[username] = request.sid
            emit("data", client_decks[username][0], to=request.sid)
        elif client_usernames[1] == username:
            client_sids[username] = request.sid
            emit("data", client_decks[username][0], to=request.sid)


@socketio.on("disconnect")
def handle_disconnect(username):
    if username in client_usernames:
        client_usernames.remove(username)


@socketio.on("message")
def handle_message(data):
    global leading_player
    username = data.get("username")
    if username == leading_player:
        stat = data.get("stat")

        non_leading_player = next(
            username for username in client_usernames if username != leading_player
        )

        leading_value = client_decks[leading_player][0].get("stats", {}).get(stat)
        non_leading_value = (
            client_decks[non_leading_player][0].get("stats", {}).get(stat)
        )

        leading_deck = client_decks[leading_player]
        non_leading_deck = client_decks[non_leading_player]

        if leading_value > non_leading_value:
            print("transfer card from non-leading to leading player")
            transfer_card(non_leading_deck, leading_deck)
            new_leading_player = leading_player

        elif non_leading_value > leading_value:
            print("transfer card from leading player to non-leading player")
            transfer_card(leading_deck, non_leading_deck)
            new_leading_player = non_leading_player

        else:
            print("both players lose their card")
            remove_both(leading_deck, non_leading_deck)
            new_leading_player = leading_player

        if client_decks[non_leading_player]:
            emit(
                "data",
                client_decks[non_leading_player][0],
                to=client_sids[non_leading_player],
            )
        else:
            emit("data", "Your deck is empty!", to=client_sids[non_leading_player])

        if client_decks[leading_player]:
            emit(
                "data", client_decks[leading_player][0], to=client_sids[leading_player]
            )
        else:
            emit("data", "Your deck is empty!", to=client_sids[leading_player])

        leading_player = new_leading_player


if __name__ == "__main__":
    initialize_decks()
    socketio.run(app)
