import pytest
from lib.database_connection import DatabaseConnection
from app import *


@pytest.fixture
def db_connection():
    conn = DatabaseConnection(test_mode=True)
    conn.connect()
    return conn


@pytest.fixture
def web_client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
