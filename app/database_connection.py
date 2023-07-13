from lib.database_connection import get_flask_database_connection
from lib.card_repository import CardRepository
import requests


class DeckHandler:
    @staticmethod
    def create_deck(app):
        with app.app_context():
            connection = get_flask_database_connection(app)
            card_repository = CardRepository(connection, requests)
            card_repository.update_all_job_availabilities()
            all_cards = card_repository.all()
            return all_cards
