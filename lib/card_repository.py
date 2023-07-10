from lib.card import Card
from dotenv import load_dotenv
import os
import requests

load_dotenv()
reed_api_key = os.getenv("REED_API_KEY")


class CardRepository:
    def __init__(self, connection, requester) -> None:
        self._connection = connection
        self.requester = requester

    def all(self):
        rows = self._connection.execute("SELECT * from cards ORDER BY id")
        cards = []
        for row in rows:
            item = {
                "id": row["id"],
                "name": row["language_name"],
                "imageUrl": "https://upload.wikimedia.org/wikipedia/commons/6/6a/JavaScript-logo.png",  # replace with actual image url
                "stats": {
                    "age": row["age"],
                    "avg_salary": row["avg_salary"],
                    "downloads": row["downloads"],
                    "popularity": row["popularity"],
                    "job_availability": row["job_availability"],
                },
            }
            cards.append(item)
        return cards

    def find_by_language_name(self, language_name):
        rows = self._connection.execute(
            "SELECT * from cards WHERE language_name = %s", [language_name]
        )
        if not rows:
            raise Exception("Coding language not listed, please try again.")
        else:
            card = rows[0]
        return Card(
            card["id"],
            card["language_name"],
            card["age"],
            card["avg_salary"],
            card["downloads"],
            card["popularity"],
            card["job_availability"],
        )

    def find_by_age(self, age):
        rows = self._connection.execute("SELECT * from cards WHERE age = %s", [age])
        if not rows:
            raise Exception("Coding age not listed, please try again.")
        else:
            card = rows[0]
        return Card(
            card["id"],
            card["language_name"],
            card["age"],
            card["avg_salary"],
            card["downloads"],
            card["popularity"],
            card["job_availability"],
        )

    def find_by_avg_salary(self, avg_salary):
        rows = self._connection.execute(
            "SELECT * from cards WHERE avg_salary = %s", [avg_salary]
        )
        if not rows:
            raise Exception("Average salary not listed, please try again.")
        else:
            card = rows[0]
        return Card(
            card["id"],
            card["language_name"],
            card["age"],
            card["avg_salary"],
            card["downloads"],
            card["popularity"],
            card["job_availability"],
        )

    def find_by_downloads(self, downloads):
        rows = self._connection.execute(
            "SELECT * from cards WHERE downloads = %s", [downloads]
        )
        if not rows:
            raise Exception("Download not listed, please try again.")
        else:
            card = rows[0]
        return Card(
            card["id"],
            card["language_name"],
            card["age"],
            card["avg_salary"],
            card["downloads"],
            card["popularity"],
            card["job_availability"],
        )

    def find_by_popularity(self, popularity):
        rows = self._connection.execute(
            "SELECT * from cards WHERE popularity = %s", [popularity]
        )
        if not rows:
            raise Exception("Popularity not listed, please try again.")
        else:
            card = rows[0]
        return Card(
            card["id"],
            card["language_name"],
            card["age"],
            card["avg_salary"],
            card["downloads"],
            card["popularity"],
            card["job_availability"],
        )

    def find_by_job_availability(self, job_availability):
        rows = self._connection.execute(
            "SELECT * from cards WHERE job_availability = %s", [job_availability]
        )
        if not rows:
            raise Exception("Job availability not listed, please try again.")
        cards = []
        for row in rows:
            item = Card(
                row["id"],
                row["language_name"],
                row["age"],
                row["avg_salary"],
                row["downloads"],
                row["popularity"],
                row["job_availability"],
            )
            cards.append(item)
        return cards

    def update_all_job_availabilities(self):
        api_url = "https://www.reed.co.uk/api/1.0/search"
        cards = self.all()

        excluded_ids = [1, 2, 3, 4, 6, 7, 11, 15]

        for card in cards:
            # Skip languages with more than 100 job postings
            id_number = card["id"]
            if id_number in excluded_ids:
                continue

            programming_language = card["name"]

            # Create Basic Authentication header
            auth_header = "Basic " + reed_api_key

            # Set the headers in the API request
            headers = {
                "Authorization": auth_header,
            }

            # Make the API request to reed.co.uk
            response = requests.get(
                api_url,
                params={"keywords": programming_language + " developer"},
                headers=headers,
            )
            if response.status_code == 200:
                job_listings = response.json()["results"]
                job_availability = len(job_listings)

                # Update the job_availability field for the current card in the database
                self.update_card_job_availability(card["id"], job_availability)
            else:
                raise Exception(f"Error: {response.status_code}")

    def update_card_job_availability(self, card_id, job_availability):
        update_query = "UPDATE cards SET job_availability = %s WHERE id = %s"
        self._connection.execute(update_query, [job_availability, card_id])
