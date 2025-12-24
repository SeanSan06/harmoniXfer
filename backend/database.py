import sqlite3

DATA_BASE = "statistics.db"

def get_connection():
    connection = sqlite3.connect(DATA_BASE)
    connection.row_factory = sqlite3.Row

    return connection