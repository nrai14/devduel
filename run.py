from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from helpers import transfer_card, remove_both_cards
from lib.database_connection import get_flask_database_connection
from lib.card_repository import CardRepository
import random
import requests
import time


class Game:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app, origins="http://localhost:5173")
        self.socketio = SocketIO(self.app, cors_allowed_origins="http://localhost:5173")

        # Game state variables
        self.leading_player = None
        self.new_leading_player = None
        self.waiting_room = []
        self.client_usernames = []
        self.client_decks = {}
        self.player_1_deck = []
        self.player_2_deck = []
        self.black_hole = []
        self.username_to_socket = {}
        self.socket_to_username = {}
        self.start_time = None
        self.duration = 10
        self.current_score = {}

        self.initialize_decks()

        # Flask routes
        self.app.route("/results")(self.get_results)
        self.app.route("/waiting_room")(self.get_waiting_room)
        self.app.route("/clear_data", methods=["POST"])(self.clear_data)

        # SocketIO event handlers
        self.socketio.on("waiting_room")(self.handle_waiting_room)
        self.socketio.on("username")(self.handle_username)
        self.socketio.on("thinking_stat")(self.handle_thinking_stat)
        self.socketio.on("message")(self.handle_message)

    def initialize_decks(self):
        with self.app.app_context():
            connection = get_flask_database_connection(self.app)
            card_repository = CardRepository(connection, requests)
            card_repository.update_all_job_availabilities()
            all_cards = card_repository.all()
            random.shuffle(all_cards)
            self.player_1_deck = all_cards[:10]
            self.player_2_deck = all_cards[10:20]

    def run(self):
        self.socketio.run(self.app)

    def get_results(self):
        return jsonify(self.current_score), 200

    def get_waiting_room(self):
        return jsonify(self.waiting_room), 200

    def clear_data(self):
        self.leading_player = None
        self.new_leading_player = None
        self.client_usernames = []
        self.client_decks = {}
        self.player_1_deck = []
        self.player_2_deck = []
        self.black_hole = []
        self.username_to_socket = {}
        self.socket_to_username = {}
        self.start_time = None
        self.duration = 10
        self.current_score = {}
        self.initialize_decks()
        return {"message": f"Data cleared successfully"}, 200

    def handle_waiting_room(self, data):
        username = data
        self.waiting_room.append(username)
        self.socketio.emit("update_users", self.waiting_room)

    def handle_username(self, data):
        username = data.get("username", None)

        if not username:
            self.socketio.emit("message", "please create a username!", to=request.sid)
            return

        if username not in self.client_usernames and len(self.client_usernames) >= 2:
            self.socketio.emit("message", "this room is full!", to=request.sid)
            return

        self.socket_to_username[request.sid] = username
        if username not in self.client_usernames:
            self.client_usernames.append(username)
            self.username_to_socket[username] = request.sid
            if self.client_usernames[0] == username:
                self.client_decks[username] = self.player_1_deck
                self.current_score[username] = 0
                self.socketio.emit("data", self.player_1_deck[0], to=request.sid)
            elif self.client_usernames[1] == username:
                self.client_decks[username] = self.player_2_deck
                self.username_to_socket[username] = request.sid
                self.current_score[username] = 0
                self.socketio.emit("data", self.player_2_deck[0], to=request.sid)
                self.leading_player = random.choice(self.client_usernames)
                self.socketio.emit(
                    "leader", True, to=self.username_to_socket[self.leading_player]
                )
                self.socketio.emit(
                    "message", f"{self.leading_player} is the leading player"
                )
                self.socketio.emit("start_timer", True)
                self.start_time = time.time()
                self.socketio.emit(
                    "countdown", (self.duration - (time.time() - self.start_time))
                )

        elif username in self.client_usernames:
            if self.client_usernames[0] == username:
                self.username_to_socket[username] = request.sid
                if self.leading_player == username:
                    self.socketio.emit("leader", True, to=request.sid)
                self.socketio.emit(
                    "data", self.client_decks[username][0], to=request.sid
                )
                if self.start_time:
                    self.socketio.emit("start_timer", True)
                    self.socketio.emit(
                        "countdown",
                        self.duration - (time.time() - self.start_time),
                        to=request.sid,
                    )
            elif self.client_usernames[1] == username:
                self.username_to_socket[username] = request.sid
                if self.leading_player == username:
                    self.socketio.emit("leader", True, to=request.sid)
                    self.socketio.emit(
                        "data", self.client_decks[username][0], to=request.sid
                    )
                if self.start_time:
                    self.socketio.emit("start_timer", True)
                    self.socketio.emit(
                        "countdown",
                        self.duration - (time.time() - self.start_time),
                        to=request.sid,
                    )

    def handle_thinking_stat(self, stat):
        username = self.socket_to_username.get(request.sid)

        if username != self.leading_player:
            return

        non_leading_player = next(
            username
            for username in self.client_usernames
            if username != self.leading_player
        )
        self.socketio.emit(
            "thinking_stat",
            f"{username} is thinking about selecting {stat} ...",
            to=self.username_to_socket[non_leading_player],
        )
        self.socketio.emit("message", "")

    def handle_message(self, data):
        if time.time() - self.start_time > self.duration:
            self.socketio.emit("result", "game over! Go to the results page")
            return

        username = data.get("username")

        if username != self.leading_player:
            return

        stat = data.get("stat", 0)

        non_leading_player = next(
            username
            for username in self.client_usernames
            if username != self.leading_player
        )

        if username == self.leading_player:
            leading_language = self.client_decks[self.leading_player][0].get("name")
            leading_value = (
                self.client_decks[self.leading_player][0].get("stats", {}).get(stat)
            )

            non_leading_language = self.client_decks[non_leading_player][0].get("name")
            non_leading_value = (
                self.client_decks[non_leading_player][0].get("stats", {}).get(stat)
            )

            leading_deck = self.client_decks[self.leading_player]
            non_leading_deck = self.client_decks[non_leading_player]

            if leading_value > non_leading_value:
                print("transfer card from non-leading to leading player")
                if len(self.client_decks[non_leading_player]) > 1:
                    self.current_score[self.leading_player] += 1
                    transfer_card(non_leading_deck, leading_deck)
                    self.new_leading_player = self.leading_player
                    emit(
                        "message",
                        f"{leading_language} {stat} > {non_leading_language}. You won this round!",
                        to=self.username_to_socket[self.leading_player],
                    )
                    emit(
                        "message",
                        f"{non_leading_language} {stat} < {leading_language}. You lost this round!",
                        to=self.username_to_socket[non_leading_player],
                    )
                else:
                    self.socketio.emit("message", "game over!")
                    self.socketio.emit(
                        "result",
                        f"{non_leading_player} has run out of cards, {self.leading_player} wins!",
                    )

            elif non_leading_value > leading_value:
                print("transfer card from leading player to non-leading player")
                if len(self.client_decks[self.leading_player]) > 1:
                    self.current_score[non_leading_player] += 1
                    transfer_card(leading_deck, non_leading_deck)
                    self.new_leading_player = non_leading_player
                    emit(
                        "message",
                        f"{non_leading_language} {stat} > {leading_language}. You won this round; you're now the leader!",
                        to=self.username_to_socket[non_leading_player],
                    )
                    emit(
                        "message",
                        f"{leading_language} {stat} < {non_leading_language}. You lost this round; you're no longer the leader!",
                        to=self.username_to_socket[self.leading_player],
                    )
                else:
                    self.socketio.emit("message", "game over!")
                    self.socketio.emit(
                        "result",
                        f"{self.leading_player} has run out of cards, {non_leading_player} wins!",
                    )

            else:
                print("both players lose their card")
                if (
                    len(self.client_decks[self.leading_player]) > 1
                    and len(self.client_decks[non_leading_player]) > 1
                ):
                    remove_both_cards(leading_deck, non_leading_deck, self.black_hole)
                    self.new_leading_player = self.leading_player
                    emit(
                        "message",
                        "It's a tie!",
                        to=self.username_to_socket[self.leading_player],
                    )
                    emit(
                        "message",
                        "It's a tie!",
                        to=self.username_to_socket[non_leading_player],
                    )
                else:
                    self.socketio.emit("message", "game over!")
                    self.socketio.emit(
                        "result", f"neither player has any more cards, it's a tie!"
                    )

        if self.new_leading_player != self.leading_player:
            emit("leader", True, to=self.username_to_socket[self.new_leading_player])
            emit("leader", False, to=self.username_to_socket[self.leading_player])

        if self.client_decks[self.leading_player]:
            emit(
                "data",
                self.client_decks[self.leading_player][0],
                to=self.username_to_socket[self.leading_player],
            )

        if self.client_decks[non_leading_player]:
            emit(
                "data",
                self.client_decks[non_leading_player][0],
                to=self.username_to_socket[non_leading_player],
            )

        self.socketio.emit(
            "update_assets",
            {
                self.leading_player: len(self.client_decks[self.leading_player]),
                non_leading_player: len(self.client_decks[non_leading_player]),
                "black_hole": len(self.black_hole),
            },
        )

        self.socketio.emit("thinking_stat", "")

        self.leading_player = self.new_leading_player


if __name__ == "__main__":
    game = Game()
    game.run()
