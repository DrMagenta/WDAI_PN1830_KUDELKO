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
    user_orders = conn.execute('SELECT id, bookId, quantity FROM orders WHERE userId = ?',
                        (userId,)).fetchall()
    conn.close()
    if user_orders is None:
        abort(404)
        
    result = []
    for order in user_orders:
        result.append({k: order[k] for k in order.keys()})
    return json.dumps(result)

@app.route('/api/orders', methods=["POST"])
def make_order():
    bookId = request.get_json().get('bookId')
    userId = request.get_json().get('userId')
    quantity = request.get_json().get('quantity')
    
    if not bookId:
        return 'A book is required!', 400

    elif not userId:
        return 'An user is required!', 400
    
    elif not quantity:
        return 'Quantity of books is required!', 400
    
    bookId = int(bookId)
    book_response = requests.get(f'http://localhost:3001/api/books/{bookId}')
    
    if book_response.status_code == 404:
        abort(404)
    else:
        conn = get_db_connection()
        conn.execute('INSERT INTO orders (userId, bookId, quantity) VALUES (?, ?, ?)',
                     (userId, bookId, quantity))
        
        max_id = conn.execute('SELECT MAX(id) AS max_id FROM orders').fetchone()
        
        
        conn.commit()
        conn.close()
        
        id = str(max_id['max_id'] + 1)
        
        return id, 200
    
@app.route("/api/orders/<int:orderId>", methods=["DELETE"])
def delete_order(orderId):
    conn = get_db_connection()
    conn.execute("DELETE FROM orders WHERE id = ?", (orderId,))
    
    conn.commit()
    conn.close()
    
    return "Order deleted", 200

    

@app.route('/api/orders/<int:orderId>', methods=["PATCH"])
def update_order(orderId):
    bookId = request.get_json().get("bookId")
    userId = request.get_json().get("userId")
    quantity = request.get_json().get("quantity")
    
    
    conn = get_db_connection()
    
    order_data = conn.execute('SELECT bookId, userId, quantity FROM orders WHERE id = ?',
                              (orderId,)).fetchone()
    
    if order_data is None:
        abort(404)
    
    order = dict(order_data)
    
    stored_userId = order['userId']
    stored_bookId = order['bookId']
    stored_quantity = order['quantity']
    
    if not bookId:
        bookId = stored_bookId
    if not userId:
        userId = stored_userId
    if not quantity:
        quantity = stored_quantity
        
    conn.execute('UPDATE orders SET bookId = ?, userId = ?, quantity = ? WHERE id = ?',
                 (bookId, userId, quantity, orderId))
    
    conn.commit()
    conn.close()
    
    return "Order updated", 200

if __name__ == '__main__':
    app.run(host="localhost", port=3002)