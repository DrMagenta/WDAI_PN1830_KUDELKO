from flask import Flask, jsonify, make_response, request, abort
import requests
import threading
import json
import jwt
import sqlite3
from functools import wraps
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello there!"

def get_db_connection():
    conn = sqlite3.connect(PROJECT_ROOT / 'database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/api/books/<int:bookId>")
def get_book(bookId):
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?',
                        (bookId,)).fetchone()
    conn.close()
    if book is None:
        abort(404)
        
    result = {k: book[k] for k in book.keys()}
    return json.dumps(result)

@app.route("/api/books")
def getBooks():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    result = []
    for item in books:
        result.append({k: item[k] for k in item.keys()})
    return json.dumps(result)


@app.route("/api/books",  methods=['POST'])
def addBook():
    title = request.get_json().get('title')
    author = request.get_json().get('author')
    year = request.get_json().get('year')
    
    if not title:
        return 'Title is required!', 400

    elif not author:
        return 'Author is required!', 400
    
    elif not year:
        return 'Year of publishment is required!', 400

    else:
        conn = get_db_connection()
        conn.execute('INSERT INTO books (title, author, year) VALUES (?, ?, ?)',
                     (title, author, year))
        
        id = conn.execute('SELECT id FROM books WHERE title = ? AND author = ?',
                     (title, author)).fetchone()
        
        id = id['id']
        conn.commit()
        conn.close()
        return f'Post was successfully added. Book ID: {id}', 200
    
@app.route("/api/books/<int:bookId>", methods=["DELETE"])
def deleteBook(bookId):
    conn = get_db_connection()
    conn.execute("DELETE FROM books WHERE id = ?", (bookId,))
    
    conn.commit()
    conn.close()
    
    return "Book deleted", 200

if __name__ == '__main__':
    app.run(host="localhost", port=3001)