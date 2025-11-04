
# database handler

import sqlite3
from passlib.hash import sha256_crypt

DB_NAME = "users.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
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
    conn.close()

def add_user(username,password):
    hashed_password = sha256_crypt.hash(password)
    
    try: 
        conn = sqlite3.connect(DB_NAME)
        c=conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                  (username, hashed_password))
        
        conn.commit()
        conn.close()

        return True, "Made user"
    except sqlite3.IntegrityError:
        return False,"User already exists in DB"
    
def check_user(username,password):
    # check if user already exists
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()

    if row and sha256_crypt.verify(password, row[0]):
        return True
    return False