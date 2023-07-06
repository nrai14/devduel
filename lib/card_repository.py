from lib.card import Card
import requests


class CardRepository:
    def __init__(self, connection) -> None:
        self._connection = connection
        # self.requester = requester

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
                    "avg_salary": row["av_salary"],
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
            card["av_salary"],
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
            card["av_salary"],
            card["downloads"],
            card["popularity"],
            card["job_availability"],
        )

    def find_by_av_salary(self, av_salary):
        rows = self._connection.execute(
            "SELECT * from cards WHERE av_salary = %s", [av_salary]
        )
        if not rows:
            raise Exception("Average salary not listed, please try again.")
        else:
            card = rows[0]
        return Card(
            card["id"],
            card["language_name"],
            card["age"],
            card["av_salary"],
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
            card["av_salary"],
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
            card["av_salary"],
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
                row["av_salary"],
                row["downloads"],
                row["popularity"],
                row["job_availability"],
            )
            cards.append(item)
        return cards

    def update_all_job_availabilities(self):
        api_url = self.requester.get(
            "https://www.reed.co.uk/api/1.0/search?keywords={keywords}"
        )
        cards = self.all()

        for card in cards:
            programming_language = card.language_name

            # Make the API request to reed.co.uk
            response = requests.get(api_url, params={"keywords": programming_language})

            if response.status_code == 200:
                job_listings = response.json()["results"]
                job_availability = len(job_listings)

                # Update the job_availability field for the current card in the database
                self.update_card_job_availability(card.id, job_availability)
            else:
                raise Exception("Error")

        return response.json()

    def update_card_job_availability(self, card_id, job_availability):
        update_query = "UPDATE cards SET job_availability = %s WHERE id = %s"
        self._connection.execute(update_query, [job_availability, card_id])
