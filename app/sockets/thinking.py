from flask import request


class ThinkingHandler:
    def __init__(self, game):
        self.game = game

    def handle_thinking_stat(self, stat):
        username = self.game.socket_to_username.get(request.sid)

        if username != self.game.leading_player:
            return

        non_leading_player = next(
            username
            for username in self.game.client_usernames
            if username != self.game.leading_player
        )
        self.game.socketio.emit(
            "thinking_stat",
            f"{username} is thinking about selecting {stat} ...",
            to=self.game.username_to_socket[non_leading_player],
        )
        self.game.socketio.emit("message", "")
