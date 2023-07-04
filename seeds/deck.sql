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
    ('Javascript', 1, 71457, 1, 1);
    ('Python', 1, 67500, 1, 1);
    ('Go', 1, 65000, 1, 1);
    ('Java', 1, 77091, 1, 1);
    ('Kotlin', 1, 41810, 1, 1);
    ('PHP', 1, 41830, 1, 1);
    ('C#', 1, 52500, 1, 1);
    ('Swift', 1, 60375, 1, 1);
    ('Assesmbly', 1, 51931, 1, 1);
    ('Ruby', 1, 70784, 1, 1);
    ('C', 51, 1, 46550, 1, 1);
    ('COBOL', 64, 1, 42842, 1, 1);
    ('Fortran', 66, 1, 47499, 1, 1);
    ('Scala', 19, 1, 47087, 1, 1);
    ('C++', 38, 1, 79475, 1, 1);
    ('OCaml', 27, 1, 142500, 1, 1);
    ('Lua', 30, 1, 38000, 1, 1);
    ('Objective-C', 39, 1, 39489 1, 1);
    ('Rust', 8, 1, 63606, 1, 1);
    ('Perl', 35, 1, 46342, 1, 1);
