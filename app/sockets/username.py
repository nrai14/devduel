from flask import request
import random
import time


class UsernameHandler:
    def __init__(self, game):
        self.game = game

    def handle_username(self, data):
        username = data.get("username", None)

        if not username:
            self.game.socketio.emit(
                "message", "please create a username!", to=request.sid
            )
            return

        if (
            username not in self.game.client_usernames
            and len(self.game.client_usernames) >= 2
        ):
            self.game.socketio.emit("message", "this room is full!", to=request.sid)
            return

        self.game.socket_to_username[request.sid] = username
        if username not in self.game.client_usernames:
            self.game.client_usernames.append(username)
            self.game.username_to_socket[username] = request.sid
            if self.game.client_usernames[0] == username:
                self.game.client_decks[username] = self.game.player_1_deck
                self.game.current_score[username] = 0
                self.game.socketio.emit(
                    "data", self.game.player_1_deck[0], to=request.sid
                )
            elif self.game.client_usernames[1] == username:
                self.game.client_decks[username] = self.game.player_2_deck
                self.game.username_to_socket[username] = request.sid
                self.game.current_score[username] = 0
                self.game.socketio.emit(
                    "data", self.game.player_2_deck[0], to=request.sid
                )
                self.game.leading_player = random.choice(self.game.client_usernames)
                self.game.socketio.emit(
                    "leader",
                    True,
                    to=self.game.username_to_socket[self.game.leading_player],
                )
                self.game.socketio.emit(
                    "message", f"{self.game.leading_player} is the leading player"
                )
                self.game.socketio.emit("start_timer", True)
                self.game.start_time = time.time()
                self.game.socketio.emit(
                    "countdown",
                    (self.game.duration - (time.time() - self.game.start_time)),
                )

        elif username in self.game.client_usernames:
            if self.game.client_usernames[0] == username:
                self.game.username_to_socket[username] = request.sid
                if self.game.leading_player == username:
                    self.game.socketio.emit("leader", True, to=request.sid)
                self.game.socketio.emit(
                    "data", self.game.client_decks[username][0], to=request.sid
                )
                if self.game.start_time:
                    self.game.socketio.emit("start_timer", True)
                    self.game.socketio.emit(
                        "countdown",
                        self.game.duration - (time.time() - self.game.start_time),
                        to=request.sid,
                    )
            elif self.game.client_usernames[1] == username:
                self.game.username_to_socket[username] = request.sid
                if self.game.leading_player == username:
                    self.game.socketio.emit("leader", True, to=request.sid)
                self.game.socketio.emit(
                    "data", self.game.client_decks[username][0], to=request.sid
                )
                if self.game.start_time:
                    self.game.socketio.emit("start_timer", True)
                    self.game.socketio.emit(
                        "countdown",
                        self.game.duration - (time.time() - self.game.start_time),
                        to=request.sid,
                    )
