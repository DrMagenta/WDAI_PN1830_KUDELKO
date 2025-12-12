from flask import Flask, jsonify, make_response, request, abort
import requests
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

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        headers = request.headers
        bearer = headers.get('Authorization')
        if not bearer:
            return make_response(jsonify({"message": "Brak tokena!"}), 401)
        
        token = bearer

        try:
            data = jwt.decode(token, 'SECRET_KEY', algorithms=['HS256'])
        except:
            return make_response(jsonify({"message": "Token niepoprawny!"}), 401)
        else:
            
            if data['public_id'] == 'admin':
                current_user = 'admin'
            else:
                conn = get_db_connection()
                
                username = data['public_id']
                
                stored_user = conn.execute('SELECT username, id FROM users WHERE username = ?',
                                               (username,)).fetchone()
                conn.commit()
                conn.close()
                
                if stored_user is None:
                    return make_response(jsonify({"message": "Niepoprawny token!"}), 401)
                else:
                    current_user = stored_user['id']
                    
            
            
        return f(*args, **kwargs, current_user=str(current_user))
    return decorator

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
@token_required
def make_order(current_user):
    bookId = request.get_json().get('bookId')
    userId = request.get_json().get('userId')
    quantity = request.get_json().get('quantity')
    
    if not bookId:
        return 'A book is required!', 400

    elif not userId:
        return 'An user is required!', 400
    
    elif not quantity:
        return 'Quantity of books is required!', 400
    
    elif userId != current_user and current_user != 'admin':
        return "Cannot modify another user's orders!", 403
    
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
        
        id = str(max_id['max_id'])
        
        return id, 200
    
@app.route("/api/orders/<int:orderId>", methods=["DELETE"])
@token_required
def delete_order(orderId, current_user):
    
    access_granted = False
    
    conn = get_db_connection()
    
    stored_order = conn.execute('SELECT userId FROM orders WHERE id = ?',
                 (orderId,)).fetchone()
    
    if current_user == 'admin' or int(current_user) == stored_order['userId']:
        access_granted = True
        conn.execute("DELETE FROM orders WHERE id = ?", (orderId,))
    
    conn.commit()
    conn.close()
    
    return ("Order deleted", 200) if access_granted else ("Cannot delete other users' orders!", 403)

    

@app.route('/api/orders/<int:orderId>', methods=["PATCH"])
@token_required
def update_order(orderId, current_user):
    bookId = request.get_json().get("bookId")
    userId = request.get_json().get("userId")
    quantity = request.get_json().get("quantity")
    access_granted = False
    
    
    conn = get_db_connection()
    
    order_data = conn.execute('SELECT bookId, userId, quantity FROM orders WHERE id = ?',
                              (orderId,)).fetchone()
    
    if order_data is None:
        conn.commit()
        conn.close()
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
        
        
    if current_user == 'admin' or int(current_user) == userId:
        access_granted = True    
        conn.execute('UPDATE orders SET bookId = ?, userId = ?, quantity = ? WHERE id = ?',
                    (bookId, userId, quantity, orderId))
    
    conn.commit()
    conn.close()
    
    return ("Order updated", 200) if access_granted else ("Cannot modify other users' orders!", 403)

if __name__ == '__main__':
    app.run(host="localhost", port=3002)