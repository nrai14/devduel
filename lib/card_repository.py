from lib.card import Card

class CardRepository:
    def __init__(self, connection) -> None:
        self._connection = connection
        
    def all(self):
        rows = self._connection.execute('SELECT * from cards ORDER BY id')
        cards = []
        for row in rows:
            item = Card(row["id"], row["language_name"], row["age"], row["av_salary"], row["downloads"], row["popularity"], row["job_availability"])
            cards.append(item)
        return cards
     
    def find_by_language_name(self, language_name):
        rows = self._connection.execute(
            'SELECT * from cards WHERE language_name = %s', [language_name])
        if not rows:
            raise Exception("Coding language not listed, please try again.")
        else:
            card = rows[0]
        return Card(
            card["id"], card["language_name"], card["age"], card["av_salary"], card["downloads"], card["popularity"], card["job_availability"]
        )
    
    def find_by_age(self, age):
        rows = self._connection.execute(
            'SELECT * from cards WHERE age = %s', [age])
        if not rows:
            raise Exception("Coding age not listed, please try again.")
        else:
            card = rows[0]
        return Card(
            card["id"], card["language_name"], card["age"], card["av_salary"], card["downloads"], card["popularity"], card["job_availability"]
        )
    
    def find_by_av_salary(self, av_salary):
        rows = self._connection.execute(
            'SELECT * from cards WHERE av_salary = %s', [av_salary])
        if not rows:
            raise Exception("Average salary not listed, please try again.")
        else:
            card = rows[0]
        return Card(
            card["id"], card["language_name"], card["age"], card["av_salary"], card["downloads"], card["popularity"], card["job_availability"]
        )
    
    def find_by_downloads(self, downloads):
        rows = self._connection.execute(
            'SELECT * from cards WHERE downloads = %s', [downloads])
        if not rows:
            raise Exception("Download not listed, please try again.")
        else:
            card = rows[0]
        return Card(
            card["id"], card["language_name"], card["age"], card["av_salary"], card["downloads"], card["popularity"], card["job_availability"]
        )
    
    def find_by_popularity(self, popularity):
        rows = self._connection.execute(
            'SELECT * from cards WHERE popularity = %s', [popularity])
        if not rows:
            raise Exception("Popularity not listed, please try again.")
        else:
            card = rows[0]
        return Card(
            card["id"], card["language_name"], card["age"], card["av_salary"], card["downloads"], card["popularity"], card["job_availability"]
        )
    
    def find_by_job_availability(self, job_availability):
        rows = self._connection.execute(
            'SELECT * from cards WHERE job_availability = %s', [job_availability])
        if not rows:
            raise Exception("Job availability not listed, please try again.")
        cards = []
        for row in rows:
             item = Card(row["id"], row["language_name"], row["age"], row["av_salary"], row["downloads"], row["popularity"], row["job_availability"])
             cards.append(item)
        return cards
    
