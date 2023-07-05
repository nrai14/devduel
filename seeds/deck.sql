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
    ('Javascript', 28, 71457, 12529489, 7, 1),
    ('Python', 32, 67500, 90232242, 1, 1),
    ('Go', 14,  65000, 9959490, 14, 1),
    ('Java', 27, 77091, 20340247, 4, 1),
    ('Kotlin', 13, 41810, 1042196, 29, 1),
    ('PHP', 29,  41830, 9475496, 8, 1),
    ('C#', 23,  52500, 22375966, 5, 1),
    ('Swift', 9,  60375, 135064, 19, 1), 
    ('Assembly', 76, 51931, 606205, 10, 1),
    ('Ruby', 28,  70784, 3365134, 18, 1),
    ('C', 51, 46550, 1, 2, 1),
    ('COBOL', 64, 42842, 1, 22, 1),
    ('Fortran', 66, 47499, 1, 15, 1),
    ('Scala', 19, 47087, 1, 35, 1),
    ('C++', 38, 79475, 48914870, 3, 1),
    ('OCaml', 27, 142500, 107877, 51, 1),
    ('Lua', 30, 38000, 850200, 32, 1),
    ('Objective-C', 39, 39489, 1, 24, 1),
    ('Rust', 8, 63606, 1, 20, 1),
    ('Perl', 35, 46342, 1, 25, 1);
