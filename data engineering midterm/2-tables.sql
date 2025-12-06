SELECT * FROM pg_stat_replication;

-- create tables
CREATE TABLE authors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    bio TEXT
);


CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    published_date DATE
);

CREATE TABLE readers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE
);


CREATE TABLE author_books (
    author_id INT NOT NULL,
    book_id INT NOT NULL,
    PRIMARY KEY (author_id, book_id),
    FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
);



CREATE TABLE book_readers (
    book_id INT NOT NULL,
    reader_id INT NOT NULL,
    PRIMARY KEY (book_id, reader_id),
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE,
    FOREIGN KEY (reader_id) REFERENCES readers(id) ON DELETE CASCADE
);

-- insert data into tables
INSERT INTO books (title, published_date)
SELECT
'Book ' || gs AS title,
date '2000-01-01' + (random() * 8035)::int AS published_date
FROM generate_series(1, 1000000) AS gs;


INSERT INTO authors (name, bio)
SELECT
'Author ' || gs AS name,
'Bio for author ' || gs AS bio
FROM generate_series(1, 1000) AS gs;


INSERT INTO author_books (author_id, book_id)
SELECT
(floor(random() * 1000 + 1))::int AS author_id,
b.id AS book_id
FROM books b;



INSERT INTO readers (name, email)
SELECT
'Reader ' || gs AS name,
'reader' || gs || '@example.com' AS email
FROM generate_series(1, 100000) AS gs;



WITH book_ids AS (
SELECT id FROM books
)
INSERT INTO book_readers (book_id, reader_id)
SELECT
b.id AS book_id,
(floor(random() * 100000 + 1))::int AS reader_id
FROM book_ids b,
LATERAL generate_series(1, (floor(random() * 5 + 1))::int);
