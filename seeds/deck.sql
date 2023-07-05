DROP TABLE IF EXISTS cards;
DROP SEQUENCE IF EXISTS cards_id_seq;

CREATE SEQUENCE IF NOT EXISTS cards_id_seq;
CREATE TABLE cards (
    id SERIAL PRIMARY KEY,
    language_name text,
    age int,
    av_salary int,
    downloads int,
    popularity int,
    job_availability int
);

INSERT INTO cards 
    (language_name, age, av_salary, downloads, popularity, job_availability) 
VALUES 
    ('Javascript', 28, 71457, 1, 1, 1),
    ('Python', 32, 67500, 1, 1, 1),
    ('Go', 14, 65000, 1, 1, 1),
    ('Java', 27, 77091, 1, 1, 1),
    ('Kotlin', 13, 41810, 1, 1, 1),
    ('PHP', 29, 41830, 1, 1, 1),
    ('C#', 23, 52500, 1, 1, 1),
    ('Swift', 9, 60375, 1, 1, 1), 
    ('Assembly', 76, 51931, 1, 1, 1),
    ('Ruby', 28, 70784, 1, 1, 1),
    ('C', 51, 46550, 1, 1, 1),
    ('COBOL', 64, 42842, 1, 1, 1),
    ('Fortran', 66, 47499, 1, 1, 1),
    ('Scala', 19, 47087, 1, 1, 1),
    ('C++', 38, 79475, 1, 1, 1),
    ('OCaml', 27, 142500, 1, 1, 1),
    ('Lua', 30, 38000, 1, 1, 1),
    ('Objective-C', 39, 39489, 1, 1, 1),
    ('Rust', 8, 63606, 1, 1, 1),
    ('Perl', 35, 46342, 1, 1, 1);
