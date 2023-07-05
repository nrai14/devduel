from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from cards import cards_player_1, cards_player_2

app = Flask(__name__)
CORS(app, origins="http://localhost:5173")
socketio = SocketIO(app, cors_allowed_origins="http://localhost:5173")
clients = []


@app.route("/")
def index():
    return "Hello, World!"


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
