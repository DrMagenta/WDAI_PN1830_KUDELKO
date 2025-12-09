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

orders_to_insert = [
    (1, 1, 1),  # użytkownik 1 zamawia 1 szt. książki 1
    (1, 3, 2),  # użytkownik 1 zamawia 2 szt. książki 3
    (2, 2, 1),  # użytkownik 2 zamawia 1 szt. książki 2
    (3, 5, 4),  # użytkownik 3 zamawia 4 szt. książki 5
    (2, 1, 1),  # użytkownik 2 zamawia 1 szt. książki 1
]

cur = connection.cursor()

cur.executemany(
    "INSERT INTO orders (userId, bookId, quantity) VALUES (?, ?, ?)",
    orders_to_insert
)

cur.executemany(
    "INSERT INTO books (title, author, year) VALUES (?, ?, ?)",
    books_to_insert
)

connection.commit()
connection.close()