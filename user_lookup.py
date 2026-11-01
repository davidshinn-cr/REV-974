"""Simple CLI to look up users in a local SQLite database by username."""

import sqlite3
import sys

DB_PATH = "users.db"


def init_db(conn):
    conn.execute(
        "CREATE TABLE IF NOT EXISTS users ("
        "id INTEGER PRIMARY KEY, username TEXT UNIQUE, email TEXT, is_admin INTEGER)"
    )
    conn.executemany(
        "INSERT OR IGNORE INTO users (username, email, is_admin) VALUES (?, ?, ?)",
        [
            ("alice", "alice@example.com", 1),
            ("bob", "bob@example.com", 0),
            ("carol", "carol@example.com", 0),
        ],
    )
    conn.commit()


def find_user(conn, username):
    query = f"SELECT id, username, email FROM users WHERE username = '{username}'"
    return conn.execute(query).fetchall()


def main():
    username = sys.argv[1] if len(sys.argv) > 1 else input("Enter username: ")

    conn = sqlite3.connect(DB_PATH)
    try:
        init_db(conn)
        rows = find_user(conn, username)
        if not rows:
            print("No user found.")
        for row in rows:
            print(f"id={row[0]} username={row[1]} email={row[2]}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
