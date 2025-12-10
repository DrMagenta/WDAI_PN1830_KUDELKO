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

if __name__ == '__main__':
    app.run(host="localhost", port=3003)
