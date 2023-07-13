from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import random

# Import socket handlers
from app.sockets.message import MessageHandler
from app.sockets.thinking import ThinkingHandler
from app.sockets.username import UsernameHandler
from app.sockets.update import UpdateHandler

# Import routes and database
from app.routes import SetupRoutes
from app.database_connection import DeckHandler


class Game:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app, origins="http://localhost:5173")
        self.socketio = SocketIO(self.app, cors_allowed_origins="http://localhost:5173")

        # Connect with db and fetch latest stat data
        self.all_cards = DeckHandler.create_deck(self.app)

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
        self.duration = 120
        self.current_score = {}

        self.initialize_decks()

        # Initialize SocketIO event handlers
        self.message_handler = MessageHandler(self)
        self.thinking_handler = ThinkingHandler(self)
        self.update_handler = UpdateHandler(self)
        self.username_handler = UsernameHandler(self)

        # Flask routes
        self.setup_routes = SetupRoutes(self)
        self.app.route("/results")(self.setup_routes.get_results)
        self.app.route("/waiting_room")(self.setup_routes.get_waiting_room)
        self.app.route("/clear_data", methods=["POST"])(self.setup_routes.clear_data)

        # SocketIO event handlers
        self.socketio.on("waiting_room")(self.update_handler.handle_waiting_room)
        self.socketio.on("username")(self.username_handler.handle_username)
        self.socketio.on("thinking_stat")(self.thinking_handler.handle_thinking_stat)
        self.socketio.on("message")(self.message_handler.handle_message)

    def run(self):
        self.socketio.run(self.app)

    def initialize_decks(self):
        random.shuffle(self.all_cards)
        self.player_1_deck = self.all_cards[:10]
        self.player_2_deck = self.all_cards[10:20]
