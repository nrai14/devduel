def transfer_card(from_deck, to_deck):
    to_deck.append(from_deck[0])
    from_deck.remove(from_deck[0])