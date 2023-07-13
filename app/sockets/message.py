from flask_socketio import emit
from app.helpers import transfer_card, remove_both_cards
import time


class MessageHandler:
    def __init__(self, game):
        self.game = game

    def handle_message(self, data):
        if time.time() - self.game.start_time > self.game.duration:
            self.game.socketio.emit("result", "game over! Go to the results page")
            return

        username = data.get("username")

        if username != self.game.leading_player:
            return

        stat = data.get("stat", 0)

        non_leading_player = next(
            username
            for username in self.game.client_usernames
            if username != self.game.leading_player
        )

        if username == self.game.leading_player:
            leading_language = self.game.client_decks[self.game.leading_player][0].get(
                "name"
            )
            leading_value = (
                self.game.client_decks[self.game.leading_player][0]
                .get("stats", {})
                .get(stat)
            )

            non_leading_language = self.game.client_decks[non_leading_player][0].get(
                "name"
            )
            non_leading_value = (
                self.game.client_decks[non_leading_player][0].get("stats", {}).get(stat)
            )

            leading_deck = self.game.client_decks[self.game.leading_player]
            non_leading_deck = self.game.client_decks[non_leading_player]

            if leading_value > non_leading_value:
                print("transfer card from non-leading to leading player")
                if len(self.game.client_decks[non_leading_player]) > 1:
                    self.game.current_score[self.game.leading_player] += 1
                    transfer_card(non_leading_deck, leading_deck)
                    self.game.new_leading_player = self.game.leading_player
                    emit(
                        "message",
                        f"{leading_language} {stat} > {non_leading_language}. You won this round!",
                        to=self.game.username_to_socket[self.game.leading_player],
                    )
                    emit(
                        "message",
                        f"{non_leading_language} {stat} < {leading_language}. You lost this round!",
                        to=self.game.username_to_socket[non_leading_player],
                    )
                else:
                    self.game.socketio.emit("message", "game over!")
                    self.game.socketio.emit(
                        "result",
                        f"{non_leading_player} has run out of cards, {self.game.leading_player} wins!",
                    )

            elif non_leading_value > leading_value:
                print("transfer card from leading player to non-leading player")
                if len(self.game.client_decks[self.game.leading_player]) > 1:
                    self.game.current_score[non_leading_player] += 1
                    transfer_card(leading_deck, non_leading_deck)
                    self.game.new_leading_player = non_leading_player
                    emit(
                        "message",
                        f"{non_leading_language} {stat} > {leading_language}. You won this round; you're now the leader!",
                        to=self.game.username_to_socket[non_leading_player],
                    )
                    emit(
                        "message",
                        f"{leading_language} {stat} < {non_leading_language}. You lost this round; you're no longer the leader!",
                        to=self.game.username_to_socket[self.game.leading_player],
                    )
                else:
                    self.game.socketio.emit("message", "game over!")
                    self.game.socketio.emit(
                        "result",
                        f"{self.game.leading_player} has run out of cards, {non_leading_player} wins!",
                    )

            else:
                print("both players lose their card")
                if (
                    len(self.game.client_decks[self.game.leading_player]) > 1
                    and len(self.game.client_decks[non_leading_player]) > 1
                ):
                    remove_both_cards(
                        leading_deck, non_leading_deck, self.game.black_hole
                    )
                    self.game.new_leading_player = self.game.leading_player
                    emit(
                        "message",
                        "It's a tie!",
                        to=self.game.username_to_socket[self.game.leading_player],
                    )
                    emit(
                        "message",
                        "It's a tie!",
                        to=self.game.username_to_socket[non_leading_player],
                    )
                else:
                    self.game.socketio.emit("message", "game over!")
                    self.game.socketio.emit(
                        "result", f"neither player has any more cards, it's a tie!"
                    )

        if self.game.new_leading_player != self.game.leading_player:
            emit(
                "leader",
                True,
                to=self.game.username_to_socket[self.game.new_leading_player],
            )
            emit(
                "leader",
                False,
                to=self.game.username_to_socket[self.game.leading_player],
            )

        if self.game.client_decks[self.game.leading_player]:
            emit(
                "data",
                self.game.client_decks[self.game.leading_player][0],
                to=self.game.username_to_socket[self.game.leading_player],
            )

        if self.game.client_decks[non_leading_player]:
            emit(
                "data",
                self.game.client_decks[non_leading_player][0],
                to=self.game.username_to_socket[non_leading_player],
            )

        self.game.socketio.emit(
            "update_assets",
            {
                self.game.leading_player: len(
                    self.game.client_decks[self.game.leading_player]
                ),
                non_leading_player: len(self.game.client_decks[non_leading_player]),
                "black_hole": len(self.game.black_hole),
            },
        )

        self.game.socketio.emit("thinking_stat", "")

        self.game.leading_player = self.game.new_leading_player
