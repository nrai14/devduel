"""
When I seed the database
I get some records back
"""


def test_database_connection(db_connection):
    db_connection.seed("seeds/database_connection.sql")

    db_connection.execute(
        "INSERT INTO test_table (name) VALUES (%s)", ["second_record"]
    )

    result = db_connection.execute("SELECT * FROM test_table")

    assert result == [
        {"id": 1, "name": "first_record"},
        {"id": 2, "name": "second_record"},
    ]
