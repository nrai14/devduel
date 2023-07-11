def transfer_card(from_deck, to_deck):
    winning_card = to_deck.pop(0)
    to_deck.append(winning_card)
    to_deck.append(from_deck[0])
    from_deck.remove(from_deck[0])


def remove_both_cards(deck, other_deck, black_hole):
    black_hole.append(deck[0])
    black_hole.append(other_deck[0])
    deck.remove(deck[0])
    other_deck.remove(deck[0])
