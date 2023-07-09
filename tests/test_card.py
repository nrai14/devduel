from lib.card import Card

"""
Card constructs with language name, age, average salary,
number of downloads, popularity and job availability
"""


def test_card_constructs():
    card = Card(1, "Test Card", 20, 45000, 3000, 5, 215)
    assert card.id == 1
    assert card.language_name == "Test Card"
    assert card.age == 20
    assert card.avg_salary == 45000
    assert card.downloads == 3000
    assert card.popularity == 5
    assert card.job_availability == 215


"""
We can format cards into strings nicely
"""


def test_cards_format_nicely():
    card = Card(1, "Test Card", 20, 45000, 3000, 5, 215)
    assert (
        str(card)
        == "Card(id=1, language_name='Test Card', age=20, avg_salary=45000, downloads=3000, popularity=5, job_availability=215)"
    )


"""
We can compare two identical cards
"""


def test_cards_are_equal():
    card_1 = Card(1, "Test Card", 20, 45000, 3000, 5, 215)
    card_2 = Card(1, "Test Card", 20, 45000, 3000, 5, 215)
    assert card_1 == card_2
