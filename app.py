from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from helpers.adjust_deck import transfer_card, remove_both_cards
from lib.database_connection import get_flask_database_connection
from lib.card_repository import CardRepository
import random
import requests
import time


app = Flask(__name__)
CORS(app, origins="http://localhost:5173")
socketio = SocketIO(app, cors_allowed_origins="http://localhost:5173")

leading_player = None
new_leading_player = None
waiting_room = []
client_usernames = []
client_decks = {}
player_1_deck = []
player_2_deck = []
black_hole = []
username_to_socket = {}
socket_to_username = {}
start_time = None
duration = 300
current_score = {}


def initialize_decks():
    global player_1_deck, player_2_deck
    with app.app_context():
        connection = get_flask_database_connection(app)
        card_repository = CardRepository(connection, requests)
        card_repository.update_all_job_availabilities()
        all_cards = card_repository.all()
        random.shuffle(all_cards)
        player_1_deck = all_cards[0:10]
        player_2_deck = all_cards[11:20]


@app.route("/results")
def get_results():
    return jsonify(current_score)

@app.route("/waitingroom")
def get_waiting_room():
    return jsonify(waiting_room)

@socketio.on("waiting_room")
def handle_waiting_players(data):
    waiting_room.append(data.get("username"))

@socketio.on("username")
def handle_username(data):
    global leading_player
    global start_time

    username = data.get("username", None)

    if not username:
        emit("message", "please create a username!", to=request.sid)
        return

    if username not in client_usernames and len(client_usernames) >= 2:
        emit("message", "this room is full!", to=request.sid)
        return

    socket_to_username[request.sid] = username

    if username not in client_usernames:
        client_usernames.append(username)
        username_to_socket[username] = request.sid
        if client_usernames[0] == username:
            client_decks[username] = player_1_deck
            current_score[username] = 0
            emit("data", player_1_deck[0], to=request.sid)
        elif client_usernames[1] == username:
            client_decks[username] = player_2_deck
            username_to_socket[username] = request.sid
            current_score[username] = 0
            emit("data", player_2_deck[0], to=request.sid)
            leading_player = random.choice(client_usernames)
            emit("leader", True, to=username_to_socket[leading_player])
            socketio.emit("message", f"{leading_player} is the leading player")
            socketio.emit("start_timer", True)
            start_time = time.time()
            socketio.emit("countdown", (duration - (time.time() - start_time)))

    elif username in client_usernames:
        if client_usernames[0] == username:
            username_to_socket[username] = request.sid
            if leading_player == username:
                emit("leader", True, to=request.sid)
            emit("data", client_decks[username][0], to=request.sid)
            if start_time:
                socketio.emit("start_timer", True)
                emit("countdown", duration - (time.time() - start_time), to=request.sid)
        elif client_usernames[1] == username:
            username_to_socket[username] = request.sid
            if leading_player == username:
                emit("leader", True, to=request.sid)
                emit("data", client_decks[username][0], to=request.sid)
            if start_time:
                socketio.emit("start_timer", True)
                emit("countdown", duration - (time.time() - start_time), to=request.sid)


# @socketio.on("disconnect")
# def handle_disconnect():
#     global leading_player
#     username = socket_to_username.get(request.sid)
#     if username in client_usernames:
#         client_usernames.remove(username)
#         if username == leading_player:
#             leading_player = next((username for username in client_usernames), None)


@socketio.on("thinking_stat")
def handle_thinking_stat(stat):
    global leading_player
    username = socket_to_username.get(request.sid)

    if username != leading_player:
        return

    non_leading_player = next(
        username for username in client_usernames if username != leading_player
    )
    emit(
        "thinking_stat",
        f"{username} is thinking about selecting {stat} ...",
        to=username_to_socket[non_leading_player],
    )
    socketio.emit("message", "")


@socketio.on("message")
def handle_message(data):
    global leading_player, new_leading_player
    if time.time() - start_time > duration:
        socketio.emit("message", "game over! Go to the results page")
        return

    username = data.get("username")

    if username != leading_player:
        return

    stat = data.get("stat", 0)

    non_leading_player = next(
        username for username in client_usernames if username != leading_player
    )

    if username == leading_player:
        leading_language = client_decks[leading_player][0].get("name")
        leading_value = client_decks[leading_player][0].get("stats", {}).get(stat)

        non_leading_language = client_decks[non_leading_player][0].get("name")
        non_leading_value = (
            client_decks[non_leading_player][0].get("stats", {}).get(stat)
        )

        leading_deck = client_decks[leading_player]
        non_leading_deck = client_decks[non_leading_player]

        if leading_value > non_leading_value:
            print("transfer card from non-leading to leading player")
            if len(client_decks[non_leading_player]) > 1:
                current_score[leading_player] += 1
                transfer_card(non_leading_deck, leading_deck)
                new_leading_player = leading_player
                emit(
                    "message",
                    f"{leading_language} {stat} > {non_leading_language}. You won this round!",
                    to=username_to_socket[leading_player],
                )
                emit(
                    "message",
                    f"{non_leading_language} {stat} < {leading_language}. You lost this round!",
                    to=username_to_socket[non_leading_player],
                )
            else:
                socketio.emit("message", "game over!")
                socketio.emit(
                    "result",
                    f"{non_leading_player} has run out of cards, {leading_player} wins!",
                )

        elif non_leading_value > leading_value:
            print("transfer card from leading player to non-leading player")
            if len(client_decks[leading_player]) > 1:
                current_score[non_leading_player] += 1
                transfer_card(leading_deck, non_leading_deck)
                new_leading_player = non_leading_player
                emit(
                    "message",
                    f"{non_leading_language} {stat} > {leading_language}. You won this round; you're now the leader!",
                    to=username_to_socket[non_leading_player],
                )
                emit(
                    "message",
                    f"{leading_language} {stat} < {non_leading_language}. You lost this round; you're no longer the leader!",
                    to=username_to_socket[leading_player],
                )
            else:
                socketio.emit("message", "game over!")
                socketio.emit(
                    "result",
                    f"{leading_player} has run out of cards, {non_leading_player} wins!",
                )

        else:
            print("both players lose their card")
            if (
                len(client_decks[leading_player]) > 1
                and len(client_decks[non_leading_player]) > 1
            ):
                remove_both_cards(leading_deck, non_leading_deck)
                new_leading_player = leading_player
                emit("message", "It's a tie!", to=username_to_socket[leading_player])
                emit(
                    "message", "It's a tie!", to=username_to_socket[non_leading_player]
                )
            else:
                socketio.emit("message", "game over!")
                socketio.emit(
                    "result", f"neither player has any more cards, it's a tie!"
                )

    if new_leading_player != leading_player:
        emit("leader", True, to=username_to_socket[new_leading_player])
        emit("leader", False, to=username_to_socket[leading_player])

    if client_decks[leading_player]:
        emit(
            "data",
            client_decks[leading_player][0],
            to=username_to_socket[leading_player],
        )

    if client_decks[non_leading_player]:
        emit(
            "data",
            client_decks[non_leading_player][0],
            to=username_to_socket[non_leading_player],
        )

    socketio.emit("thinking_stat", "")

    leading_player = new_leading_player


if __name__ == "__main__":
    initialize_decks()
    socketio.run(app)
