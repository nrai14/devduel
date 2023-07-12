from flask import jsonify, request
from . import (
    app,
    create_app,
    initialize_decks,
    leading_player,
    new_leading_player,
    waiting_room,
)


def init_app(app):
    @app.route("/results")
    def get_results():
        return jsonify(current_score)

    @app.route("/waiting_room")
    def get_waiting_room():
        return jsonify(waiting_room)

    @app.route("/clear_data", methods=["POST"])
    def clear_data():
        global leading_player, new_leading_player, waiting_room, client_usernames, client_decks, player_1_deck, player_2_deck, black_hole, username_to_socket, socket_to_username, start_time, duration, current_score
        leading_player = None
        new_leading_player = None
        client_usernames = []
        client_decks = {}
        player_1_deck = []
        player_2_deck = []
        black_hole = []
        username_to_socket = {}
        socket_to_username = {}
        start_time = None
        duration = 10
        current_score = {}
        initialize_decks()
        return {"message": "Data cleared successfully"}, 200
