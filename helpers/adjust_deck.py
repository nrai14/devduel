def transfer_card(from_deck, to_deck):
    winning_card = to_deck.pop(0)
    to_deck.append(winning_card)
    to_deck.append(from_deck[0])
    from_deck.remove(from_deck[0])


def remove_both(deck, other_deck):
    deck = deck[1:]
    other_deck = other_deck[1:]
