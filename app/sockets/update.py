class UpdateHandler:
    def __init__(self, game):
        self.game = game

    def handle_waiting_room(self, data):
        username = data
        self.game.waiting_room.append(username)
        self.game.socketio.emit("update_users", self.game.waiting_room)
