
# database handler
import sqlite3
from passlib.hash import sha256_crypt

DB_NAME = "users.db"


def init_db():
    """Initialize the database and create users table if not exists."""
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute(
            '''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
            '''
        )
        conn.commit()


def add_user(username, password):
    
    hashed_password = sha256_crypt.hash(password)
    try:
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password)
            )
        return True, "User created successfully"
    except sqlite3.IntegrityError:
        return False, "User already exists in DB"


def check_user(username, password):
   
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT password FROM users WHERE username=?", (username,))
        row = c.fetchone()
    if row and sha256_crypt.verify(password, row[0]):
        return True
    return False


def get_user(username):
   
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT id, username, password FROM users WHERE username=?", (username,))
        row = c.fetchone()
    if row:
        return {"id": row[0], "username": row[1], "password": row[2]}
    return None
