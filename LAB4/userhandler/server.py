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

@app.route("/api/users")
def getPosts():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    result = []
    for item in posts:
      result.append({k: item[k] for k in item.keys()})
    return json.dumps(result)

@app.route('/api/register', methods=["POST"])
def register_user():
    username = request.get_json().get("username")
    email = request.get_json().get('email')
    password = request.get_json().get('password')
    
    if not username:
        return 'Username is required!', 400
    
    elif not email:
        return 'Email is required!', 400

    elif not password:
        return 'Password is required!', 400

    else:
        conn = get_db_connection()
        conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                     (username, email, password))
        
        id = conn.execute('SELECT id FROM users WHERE email = ? AND username = ?',
                     (email, username)).fetchone()
        
        id = id['id']
        conn.commit()
        conn.close()
        return f'User was successfully added. User ID: {id}', 200
    
@app.route("/api/login",  methods = ['POST'])
def login():
    auth = request.get_json()
    if not auth or not auth.get('username') or not auth.get('password'):
        return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic-realm= "Login required!"'})

    if auth.get('username') == 'admin' and auth.get('password') == 'Test1234!':
        token = jwt.encode({'public_id': 'admin'}, 'SECRET_KEY', 'HS256')
        return make_response(jsonify({'token': token}), 201)
    
    else:
        conn = get_db_connection()
        
        user_data = conn.execute('SELECT * FROM users WHERE username = ?',
                                 (auth.get('username'),) ).fetchone()
        
        conn.commit()
        conn.close()
        
        if user_data is None:
            return 'User not found!', 404
        
        user_password = user_data['password']
        
        if auth.get('password') == user_password:
            token = jwt.encode({'public_id': auth.get('username')}, 'SECRET_KEY', 'HS256')
            return make_response(jsonify({'token': token}), 201)
        

    return make_response('Could not verify password!', 403, {'WWW-Authenticate': 'Basic-realm= "Wrong Password!"'})

if __name__ == '__main__':
    app.run(host="localhost", port=3003)
