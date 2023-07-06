from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from cards import cards_player_1, cards_player_2

load_dotenv()

app = Flask(__name__)
CORS(app, origins="http://localhost:5173")
socketio = SocketIO(app, cors_allowed_origins="http://localhost:5173")

leading_player = None
client_usernames = []
client_decks = {}

@socketio.on("username")
def handle_username(username):
    global leading_player
    if username not in client_usernames:
        client_usernames.append(username)
        if client_usernames[0] == username:
            leading_player = username
            client_decks[username] = cards_player_1
            emit("data", cards_player_1[0], to=request.sid)
        elif client_usernames[1] == username:
            client_decks[username] = cards_player_2
            emit("data", cards_player_2[0], to=request.sid)

    elif username in client_usernames:
        if client_usernames[0] == username:
            emit("data", client_decks[username][0], to=request.sid)
        elif client_usernames[1] == username:
            emit("data", client_decks[username][0], to=request.sid)


@socketio.on("disconnect")
def handle_disconnect(username):
    if username in client_usernames:
        client_usernames.remove(username)

# Attribute selected by leading player
@socketio.on("message")
def handle_message(data):
    # React: stop sending username?
    losing_player = next(username for username in client_usernames if username != leading_player)
    stat = data.get("stat")
    print(losing_player)

    # access value of top card with given key for leading player
    leading_top_card = client_decks[leading_player][0]
    leading_value = leading_top_card.get("stats").get(stat)
    
    # access value of top card with given key for other player
    losing_top_card = client_decks[losing_player][0]
    losing_value = losing_top_card.get("stats").get(stat)
    print(leading_value > losing_value)
    



if __name__ == "__main__":
    socketio.run(app)
