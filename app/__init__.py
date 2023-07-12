from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from app.helpers import transfer_card, remove_both_cards
from lib.database_connection import get_flask_database_connection
from lib.card_repository import CardRepository
import random
import requests
import time


def create_app():
    app = Flask(__name__)
    CORS(app, origins="http://localhost:5173")
    socketio = SocketIO(app, cors_allowed_origins="http://localhost:5173")

    from .routes import init_app
    from .socket_handlers import init_app

    init_app(app)
    init_app(socketio)

    return app, socketio


app, socketio = create_app()

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
duration = 10
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
