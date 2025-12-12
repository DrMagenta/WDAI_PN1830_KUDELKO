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

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        headers = request.headers
        bearer = headers.get('Authorization')
        if not bearer:
            return make_response(jsonify({"message": "Brak tokena!"}), 401)

        token = bearer#.split(".")[1] 

        try:
            data = jwt.decode(token, 'SECRET_KEY', algorithms=['HS256'])
            if data['public_id'] != 'admin':
                return make_response(jsonify({"message": "Niepoprawny token!"}), 401)
            current_user = 'admin'
        except:
            return make_response(jsonify({"message": "Token niepoprawny!"}), 401)
        return f(*args, **kwargs)
    return decorator

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
@token_required
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
        return f'Book was successfully added. Book ID: {id}', 200
    
@app.route("/api/books/<int:bookId>", methods=["DELETE"])
@token_required
def deleteBook(bookId):
    conn = get_db_connection()
    conn.execute("DELETE FROM books WHERE id = ?", (bookId,))
    
    conn.commit()
    conn.close()
    
    return "Book deleted", 200

if __name__ == '__main__':
    app.run(host="localhost", port=3001)