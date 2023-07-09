from dataclasses import dataclass


@dataclass
class Card:
    id: int
    language_name: str
    age: int
    avg_salary: int
    downloads: int
    popularity: int
    job_availability: int
