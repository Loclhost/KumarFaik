import sqlite3
from typing import List, Tuple

def create_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (login TEXT, password TEXT, balance TEXT, two_factor_key TEXT, validity_flag INTEGER, update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  PRIMARY KEY (login, password))''')
    conn.commit()
    conn.close()

def check_user(login: str, password: str) -> bool:
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE login=? AND password=?", (login, password))
    result = c.fetchone()
    conn.close()
    return result is not None

def add_user(login: str, password: str, balance: str, two_factor_key: str, validity_flag: int):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (login, password, balance, two_factor_key, validity_flag) VALUES (?, ?, ?, ?, ?)",
              (login, password, balance, two_factor_key, validity_flag))
    conn.commit()
    conn.close()


def get_valid_users() -> List[Tuple]:
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE validity_flag=1")
    result = c.fetchall()
    conn.close()
    return result

def get_all_users() -> List[Tuple]:
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    result = c.fetchall()
    conn.close()
    return result

