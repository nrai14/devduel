from flask import jsonify


class SetupRoutes:
    def __init__(self, game):
        self.game = game

    def get_results(self):
        return jsonify(self.game.current_score), 200

    def get_waiting_room(self):
        return jsonify(self.game.waiting_room), 200

    def clear_data(self):
        self.game.leading_player = None
        self.game.new_leading_player = None
        self.game.client_usernames = []
        self.game.client_decks = {}
        self.game.player_1_deck = []
        self.game.player_2_deck = []
        self.game.black_hole = []
        self.game.username_to_socket = {}
        self.game.socket_to_username = {}
        self.game.start_time = None
        self.game.duration = 10
        self.game.current_score = {}
        self.game.initialize_decks()
        return {"message": f"Data cleared successfully"}, 200
