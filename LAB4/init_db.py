import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

books_to_insert = [
    ("Dune", "Frank Herbert", 1965),
    ("The Hobbit", "J.R.R. Tolkien", 1937),
    ("Neuromancer", "William Gibson", 1984),
    ("Brave New World", "Aldous Huxley", 1932),
    ("Fahrenheit 451", "Ray Bradbury", 1953)
]

cur = connection.cursor()

cur.executemany(
    "INSERT INTO books (title, author, year) VALUES (?, ?, ?)",
    books_to_insert
)

connection.commit()
connection.close()