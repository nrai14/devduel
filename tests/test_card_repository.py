from lib.card import Card
from lib.card_repository import CardRepository

def test_all(db_connection):
    db_connection.seed("seeds/deck.sql")
    repository = CardRepository(db_connection)
    assert repository.all() == [
        Card(1, 'Javascript', 1, 71457, 1, 1),
        Card(2, 'Python', 1, 67500, 1, 1),
        Card(3, 'Go', 1, 65000, 1, 1),
        Card(4, 'Java', 1, 77091, 1, 1),
        Card(5, 'Kotlin', 1, 41810, 1, 1),
        Card(6, 'PHP', 1, 41830, 1, 1),
        Card(7, 'C#', 1, 52500, 1, 1),
        Card(8, 'Swift', 1, 60375, 1, 1),
        Card(9, 'Assesmbly', 1, 51931, 1, 1),
        Card(10, 'Ruby', 1, 70784, 1, 1),
        Card(11, 'C', 51, 1, 46550, 1, 1),
        Card(12, 'COBOL', 64, 1, 42842, 1, 1),
        Card(13, 'Fortran', 66, 1, 47499, 1, 1),
        Card(14, 'Scala', 19, 1, 47087, 1, 1),
        Card(15, 'C++', 38, 1, 79475, 1, 1),
        Card(16, 'OCaml', 27, 1, 142500, 1, 1),
        Card(17, 'Lua', 30, 1, 38000, 1, 1),
        Card(18, 'Objective-C', 39, 1, 39489, 1, 1),
        Card(19, 'Rust', 8, 1, 63606, 1, 1),
        Card(20, 'Perl', 35, 1, 46342, 1, 1)
    ]