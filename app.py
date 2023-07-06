from flask import Flask, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from cards import cards_player_1, cards_player_2
from helpers.transfer_card import transfer_card

app = Flask(__name__)
CORS(app, origins="http://localhost:5173")
socketio = SocketIO(app, cors_allowed_origins="http://localhost:5173")

leading_player = None
client_usernames = []
client_decks = {}
client_sids = {}


@socketio.on("username")
def handle_username(username):
    global leading_player
    if username not in client_usernames:
        client_usernames.append(username)
        client_sids[username] = request.sid
        if client_usernames[0] == username:
            leading_player = username
            client_decks[username] = cards_player_1
            emit("data", cards_player_1[0], to=request.sid)
        elif client_usernames[1] == username:
            client_decks[username] = cards_player_2
            client_sids[username] = request.sid
            emit("data", cards_player_2[0], to=request.sid)

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
    stat = data.get("stat")
    non_leading_player = next(
        username for username in client_usernames if username != leading_player
    )
    leading_value = client_decks[leading_player][0].get("stats", {}).get(stat)
    non_leading_value = client_decks[non_leading_player][0].get("stats", {}).get(stat)

    emit(
        "data", client_decks[non_leading_player][1], to=client_sids[non_leading_player]
    )
    emit("data", client_decks[leading_player][1], to=client_sids[leading_player])


if __name__ == "__main__":
    socketio.run(app)
