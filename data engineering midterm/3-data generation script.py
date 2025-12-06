import psycopg2
from psycopg2.extras import execute_values
import random
from datetime import datetime, timedelta

# 1. Database Connection
# ----------------------
conn = psycopg2.connect(
    dbname="postgres",
    user="beqa",
    password="postgres",
    host="localhost",
    port="55432"
)
cur = conn.cursor()

print("Generating Authors...")
authors = [("Author {}".format(i), "Bio for author {}".format(i)) for i in range(1, 1001)]

execute_values(cur, "INSERT INTO authors (name, bio) VALUES %s", authors)
conn.commit()

print("Generating Books...")
books = []
base_date = datetime(2000, 1, 1)

for i in range(1, 1000001):
    title = "Book {}".format(i)
    pub_date = base_date + timedelta(days=random.randint(0, 8035))
    books.append((title, pub_date))

    if i % 10000 == 0:
        execute_values(cur, "INSERT INTO books (title, published_date) VALUES %s", books)
        books = []
        conn.commit()


print("Generating Readers...")
readers = [("Reader {}".format(i), "reader{}@example.com".format(i)) for i in range(1, 100001)]
execute_values(cur, "INSERT INTO readers (name, email) VALUES %s", readers)
conn.commit()


print("Linking Authors and Books...")
cur.execute("SELECT id FROM books")
book_ids = [row[0] for row in cur.fetchall()]

author_books = [(random.randint(1, 1000), bid) for bid in book_ids]

execute_values(cur, "INSERT INTO author_books (author_id, book_id) VALUES %s", author_books)
conn.commit()


print("Linking Readers and Books...")
cur.execute("SELECT id FROM readers")
reader_ids = [row[0] for row in cur.fetchall()]

batch = []
for bid in book_ids:
    for _ in range(random.randint(1, 5)):
        batch.append((bid, random.choice(reader_ids)))

    if len(batch) > 50000:
        execute_values(cur, "INSERT INTO book_readers (book_id, reader_id) VALUES %s", batch)
        batch = []
        conn.commit()

cur.close()
conn.close()
print("Data generation complete.")