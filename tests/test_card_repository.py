import pytest
from lib.card import Card
from lib.card_repository import CardRepository, requests

"""
When I call #all
I get a list of all cards
"""


def test_all(db_connection):
    db_connection.seed("seeds/deck.sql")
    repository = CardRepository(db_connection)
    assert repository.all() == [
        Card(1, "Javascript", 28, 71457, 12529489, 15, 1),
        Card(2, "Python", 32, 67500, 90232242, 20, 1),
        Card(3, "Go", 14, 65000, 9959490, 12, 1),
        Card(4, "Java", 27, 77091, 20340247, 17, 1),
        Card(5, "Kotlin", 13, 41810, 1042196, 4, 1),
        Card(6, "PHP", 29, 41830, 9475496, 14, 1),
        Card(7, "CSharp", 23, 52500, 22375966, 16, 1),
        Card(8, "Swift", 9, 60375, 135064, 9, 1),
        Card(9, "Assembly", 76, 51931, 606205, 13, 1),
        Card(10, "Ruby", 28, 70784, 3365134, 10, 1),
        Card(11, "C", 51, 46550, 25457435, 19, 1),
        Card(12, "COBOL", 64, 42842, 50825, 7, 1),
        Card(13, "Fortran", 66, 47499, 310454, 11, 1),
        Card(14, "Scala", 19, 47087, 688777, 2, 1),
        Card(15, "C++", 38, 79475, 23457435, 18, 1),
        Card(16, "OCaml", 27, 142500, 107877, 1, 1),
        Card(17, "Lua", 30, 38000, 850200, 3, 1),
        Card(18, "Julia", 39, 44345, 537791, 5, 1),
        Card(19, "Rust", 8, 63606, 1969477, 8, 1),
        Card(20, "Perl", 35, 46342, 148867, 6, 1),
    ]


"""
When I call #find_by_language_name
I should get one programming language back
"""


def test_find_by_language_name(db_connection):
    db_connection.seed("seeds/deck.sql")
    repository = CardRepository(db_connection)
    card = repository.find_by_language_name("Javascript")
    expected_card = Card(1, "Javascript", 28, 71457, 12529489, 15, 1)
    assert card == expected_card


"""
When I call #find_by_age
I should the age of one programming language
"""


def test_find_by_age(db_connection):
    db_connection.seed("seeds/deck.sql")
    repository = CardRepository(db_connection)
    card = repository.find_by_age(32)
    expected_card = Card(2, "Python", 32, 67500, 90232242, 20, 1)
    assert card == expected_card


"""
When I call #find_by_avg_salary
I should get one average salary for a programming language
"""


def test_find_by_avg_salary(db_connection):
    db_connection.seed("seeds/deck.sql")
    repository = CardRepository(db_connection)
    card = repository.find_by_avg_salary(60375)
    expected_card = Card(8, "Swift", 9, 60375, 135064, 9, 1)
    assert card == expected_card


"""
When I call #find_by_downloads
I should get one programming language back
"""


def test_find_by_downloads(db_connection):
    db_connection.seed("seeds/deck.sql")
    repository = CardRepository(db_connection)
    card = repository.find_by_downloads(9475496)
    expected_card = Card(6, "PHP", 29, 41830, 9475496, 14, 1)
    assert card == expected_card


"""
When I call #find_by_job_availability
I should get one programming language back
"""


def test_find_by_job_availability(db_connection):
    db_connection.seed("seeds/deck.sql")
    repository = CardRepository(db_connection)
    cards = repository.find_by_job_availability(1)
    expected_cards = [
        Card(1, "Javascript", 28, 71457, 12529489, 15, 1),
        Card(2, "Python", 32, 67500, 90232242, 20, 1),
        Card(3, "Go", 14, 65000, 9959490, 12, 1),
        Card(4, "Java", 27, 77091, 20340247, 17, 1),
        Card(5, "Kotlin", 13, 41810, 1042196, 4, 1),
        Card(6, "PHP", 29, 41830, 9475496, 14, 1),
        Card(7, "CSharp", 23, 52500, 22375966, 16, 1),
        Card(8, "Swift", 9, 60375, 135064, 9, 1),
        Card(9, "Assembly", 76, 51931, 606205, 13, 1),
        Card(10, "Ruby", 28, 70784, 3365134, 10, 1),
        Card(11, "C", 51, 46550, 25457435, 19, 1),
        Card(12, "COBOL", 64, 42842, 50825, 7, 1),
        Card(13, "Fortran", 66, 47499, 310454, 11, 1),
        Card(14, "Scala", 19, 47087, 688777, 2, 1),
        Card(15, "C++", 38, 79475, 23457435, 18, 1),
        Card(16, "OCaml", 27, 142500, 107877, 1, 1),
        Card(17, "Lua", 30, 38000, 850200, 3, 1),
        Card(18, "Julia", 39, 44345, 537791, 5, 1),
        Card(19, "Rust", 8, 63606, 1969477, 8, 1),
        Card(20, "Perl", 35, 46342, 148867, 6, 1),
    ]
    assert cards == expected_cards


"""
When we call CardRepository #find_by_language_name that's not avaliable
Raised Exception error
"""


def tests_get_language_name_that_is_not_listed(db_connection):
    db_connection.seed("seeds/deck.sql")
    repository = CardRepository(db_connection)

    with pytest.raises(Exception) as err:
        repository.find_by_language_name("BF")
    error_message = str(err.value)
    assert error_message == "Coding language not listed, please try again."


"""
When we call CardRepository #find_by_age that's not avaliable
Raised Exception error
"""


def tests_get_age_that_is_not_listed(db_connection):
    db_connection.seed("seeds/deck.sql")
    repository = CardRepository(db_connection)

    with pytest.raises(Exception) as err:
        repository.find_by_age(100)
    error_message = str(err.value)
    assert error_message == "Coding age not listed, please try again."


"""
When we call CardRepository #find_by_avg_salary that's not avaliable
Raised Exception error
"""


def tests_get_avg_salary_that_is_not_listed(db_connection):
    db_connection.seed("seeds/deck.sql")
    repository = CardRepository(db_connection)

    with pytest.raises(Exception) as err:
        repository.find_by_avg_salary(1000000)
    error_message = str(err.value)
    assert error_message == "Average salary not listed, please try again."


"""
When we call CardRepository #find_by_downloads that's not avaliable
Raised Exception error
"""


def tests_get_downloads_that_is_not_listed(db_connection):
    db_connection.seed("seeds/deck.sql")
    repository = CardRepository(db_connection)

    with pytest.raises(Exception) as err:
        repository.find_by_downloads(394329746847)
    error_message = str(err.value)
    assert error_message == "Download not listed, please try again."


"""
When we call CardRepository #find_by_popularity that's not avaliable
Raised Exception error
"""


def tests_get_popularity_that_is_not_listed(db_connection):
    db_connection.seed("seeds/deck.sql")
    repository = CardRepository(db_connection)

    with pytest.raises(Exception) as err:
        repository.find_by_popularity(394329746847)
    error_message = str(err.value)
    assert error_message == "Popularity not listed, please try again."
