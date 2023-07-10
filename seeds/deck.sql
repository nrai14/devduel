DROP TABLE IF EXISTS cards;
DROP SEQUENCE IF EXISTS cards_id_seq;

CREATE SEQUENCE IF NOT EXISTS cards_id_seq;
CREATE TABLE cards (
    id SERIAL PRIMARY KEY,
    language_name text,
    age int,
    avg_salary int,
    downloads int,
    popularity int,
    job_availability int
);

INSERT INTO cards
    (language_name, age, avg_salary, downloads, popularity, job_availability)
VALUES
    ('Javascript', 28, 71457, 12529489, 15, 1700),
    ('Python', 32, 67500, 90232242, 20, 875),
    ('Go', 14,  65000, 9959490, 12, 315),
    ('Java', 27, 77091, 20340247, 17, 750),
    ('Kotlin', 13, 41810, 1042196, 4, 4),
    ('PHP', 29, 41830, 9475496, 14, 475),
    ('C#', 23, 52500, 22375966, 16, 600),
    ('Swift', 9, 60375, 135064, 9, 9),
    ('Assembly', 76, 51931, 606205, 13, 13),
    ('Ruby', 28, 70784, 3365134, 10, 10),
    ('C', 51, 46550, 25457435, 19, 700),
    ('COBOL', 64, 42842, 50825, 7, 7),
    ('Fortran', 66, 47499, 310454, 11, 11),
    ('Scala', 19, 47087, 688777, 2, 2),
    ('C++', 38, 79475, 23457435, 18, 650),
    ('OCaml', 27, 142500, 107877, 1, 1),
    ('Lua', 30, 38000, 850200, 3, 3),
    ('Julia', 39, 44345, 537791, 5, 5),
    ('Rust', 8, 63606, 1969477, 8, 8),
    ('Perl', 35, 46342, 148867, 6, 6);
