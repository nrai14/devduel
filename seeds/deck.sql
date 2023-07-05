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
    ('Javascript', 28, 71457, 12529489, 15, 1),
    ('Python', 32, 67500, 90232242, 20, 1),
    ('Go', 14,  65000, 9959490, 12, 1),
    ('Java', 27, 77091, 20340247, 17, 1),
    ('Kotlin', 13, 41810, 1042196, 4, 1),
    ('PHP', 29, 41830, 9475496, 14, 1),
    ('C#', 23, 52500, 22375966, 16, 1),
    ('Swift', 9, 60375, 135064, 9, 1),
    ('Assembly', 76, 51931, 606205, 13, 1),
    ('Ruby', 28, 70784, 3365134, 10, 1),
    ('C', 51, 46550, 25457435, 19, 1),
    ('COBOL', 64, 42842, 50825, 7, 1),
    ('Fortran', 66, 47499, 310454, 11, 1),
    ('Scala', 19, 47087, 688777, 2, 1),
    ('C++', 38, 79475, 23457435, 18, 1),
    ('OCaml', 27, 142500, 107877, 1, 1),
    ('Lua', 30, 38000, 850200, 3, 1),
    ('Julia', 39, 44345, 537791, 5, 1),
    ('Rust', 8, 63606, 1969477, 8, 1),
    ('Perl', 35, 46342, 148867, 6, 1);
