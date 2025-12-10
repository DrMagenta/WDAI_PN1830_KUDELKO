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

def get_db_connection():
    conn = sqlite3.connect(PROJECT_ROOT / 'database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/register', methods=["POST"])
def register_user():
    email = request.get_json().get('email')
    password = request.get_json().get('password')
    
    if not email:
        return 'Email is required!', 400

    elif not password:
        return 'Password is required!', 400

    else:
        conn = get_db_connection()
        conn.execute('INSERT INTO users (email, password) VALUES (?, ?)',
                     (email, password))
        
        id = conn.execute('SELECT id FROM users WHERE email = ? AND password = ?',
                     (email, password)).fetchone()
        
        id = id['id']
        conn.commit()
        conn.close()
        return f'User was successfully added. User ID: {id}', 200

if __name__ == '__main__':
    app.run(host="localhost", port=3003)
