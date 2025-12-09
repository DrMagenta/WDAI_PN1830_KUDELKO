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

@app.route("/api/orders/<int:userId>")
def get_user_orders(userId):
    conn = get_db_connection()
    user_orders = conn.execute('SELECT bookId FROM orders WHERE userId = ?',
                        (userId,)).fetchall()
    conn.close()
    if user_orders is None:
        abort(404)
        
    result = []
    for order in user_orders:
        result.append({k: order[k] for k in order.keys()})
    return json.dumps(result)

if __name__ == '__main__':
    app.run(host="localhost", port=3002)