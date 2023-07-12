from flask import request
from flask_socketio import emit
import random
import time
from . import (
    app,
    socketio,
    create_app,
    initialize_decks,
    leading_player,
    new_leading_player,
    waiting_room,
    client_usernames,
    client_decks,
    player_1_deck,
    player_2_deck,
    black_hole,
    username_to_socket,
    socket_to_username,
    start_time,
    duration,
    current_score,
    remove_both_cards,
    transfer_card,
)


@socketio.on("waiting_room")
def handle_username(data):
    username = data
    waiting_room.append(username)
    socketio.emit("update_users", waiting_room)


@socketio.on("username")
def handle_username(data):
    global leading_player
    global start_time

    username = data.get("username", None)

    if not username:
        emit("message", "please create a username!", to=request.sid)
        return

    if username not in client_usernames and len(client_usernames) >= 2:
        emit("message", "this room is full!", to=request.sid)
        return

    socket_to_username[request.sid] = username

    if username not in client_usernames:
        client_usernames.append(username)
        username_to_socket[username] = request.sid
        if client_usernames[0] == username:
            client_decks[username] = player_1_deck
            current_score[username] = 0
            emit("data", player_1_deck[0], to=request.sid)
        elif client_usernames[1] == username:
            client_decks[username] = player_2_deck
            username_to_socket[username] = request.sid
            current_score[username] = 0
            emit("data", player_2_deck[0], to=request.sid)
            leading_player = random.choice(client_usernames)
            emit("leader", True, to=username_to_socket[leading_player])
            socketio.emit("message", f"{leading_player} is the leading player")
            socketio.emit("start_timer", True)
            start_time = time.time()
            socketio.emit("countdown", (duration - (time.time() - start_time)))

    elif username in client_usernames:
        if client_usernames[0] == username:
            username_to_socket[username] = request.sid
            if leading_player == username:
                emit("leader", True, to=request.sid)
            emit("data", client_decks[username][0], to=request.sid)
            if start_time:
                socketio.emit("start_timer", True)
                emit("countdown", duration - (time.time() - start_time), to=request.sid)
        elif client_usernames[1] == username:
            username_to_socket[username] = request.sid
            if leading_player == username:
                emit("leader", True, to=request.sid)
                emit("data", client_decks[username][0], to=request.sid)
            if start_time:
                socketio.emit("start_timer", True)
                emit("countdown", duration - (time.time() - start_time), to=request.sid)


@socketio.on("thinking_stat")
def handle_thinking_stat(stat):
    global leading_player
    username = socket_to_username.get(request.sid)

    if username != leading_player:
        return

    non_leading_player = next(
        username for username in client_usernames if username != leading_player
    )
    emit(
        "thinking_stat",
        f"{username} is thinking about selecting {stat} ...",
        to=username_to_socket[non_leading_player],
    )
    socketio.emit("message", "")


@socketio.on("message")
def handle_message(data):
    global leading_player, new_leading_player
    if time.time() - start_time > duration:
        socketio.emit("result", f"game over! Go to the results page")
        return

    username = data.get("username")

    if username != leading_player:
        return

    stat = data.get("stat", 0)

    non_leading_player = next(
        username for username in client_usernames if username != leading_player
    )

    if username == leading_player:
        leading_language = client_decks[leading_player][0].get("name")
        leading_value = client_decks[leading_player][0].get("stats", {}).get(stat)

        non_leading_language = client_decks[non_leading_player][0].get("name")
        non_leading_value = (
            client_decks[non_leading_player][0].get("stats", {}).get(stat)
        )

        leading_deck = client_decks[leading_player]
        non_leading_deck = client_decks[non_leading_player]

        if leading_value > non_leading_value:
            print("transfer card from non-leading to leading player")
            if len(client_decks[non_leading_player]) > 1:
                current_score[leading_player] += 1
                transfer_card(non_leading_deck, leading_deck)
                new_leading_player = leading_player
                emit(
                    "message",
                    f"{leading_language} {stat} > {non_leading_language}. You won this round!",
                    to=username_to_socket[leading_player],
                )
                emit(
                    "message",
                    f"{non_leading_language} {stat} < {leading_language}. You lost this round!",
                    to=username_to_socket[non_leading_player],
                )
            else:
                socketio.emit("message", "game over!")
                socketio.emit(
                    "result",
                    f"{leading_player} has run out of cards, {non_leading_player} wins!",
                )

        elif non_leading_value == leading_value:
            print("remove both cards")
            remove_both_cards(leading_deck, non_leading_deck)
            emit(
                "message",
                f"{leading_language} {stat} = {non_leading_language}. It's a draw; both cards are removed!",
                to=username_to_socket[non_leading_player],
            )
            emit(
                "message",
                f"{non_leading_language} {stat} = {leading_language}. It's a draw; both cards are removed!",
                to=username_to_socket[leading_player],
            )
            if (
                len(client_decks[leading_player]) == 0
                and len(client_decks[non_leading_player]) == 0
            ):
                socketio.emit("message", "game over!")
                socketio.emit(
                    "result",
                    "It's a draw; both players have run out of cards!",
                )

        leading_player = new_leading_player
        emit("leader", False, to=username_to_socket[leading_player])
        emit("leader", True, to=username_to_socket[leading_player])
        emit(
            "data",
            client_decks[leading_player][0],
            to=username_to_socket[leading_player],
        )
        emit(
            "data",
            client_decks[non_leading_player][0],
            to=username_to_socket[non_leading_player],
        )
        socketio.emit("message", f"{leading_player} is the new leading player")
        socketio.emit("start_timer", True)
        start_time = time.time()
        socketio.emit("countdown", (duration - (time.time() - start_time)))


if __name__ == "__main__":
    socketio.run(app, debug=True)
