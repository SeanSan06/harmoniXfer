import sqlite3

DATA_BASE = "statistics.db"

def get_connection():
    connection = sqlite3.connect(DATA_BASE)
    connection.row_factory = sqlite3.Row

    return connection

def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS statistics (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            total_songs_transferred INTEGER NOT NULL DEFAULT 0,
            total_playlists_transferred INTEGER NOT NULL DEFAULT 0,
            total_time_saved REAL NOT NULL DEFAULT 0,
            avg_time_per_song REAL NOT NULL DEFAULT 0
        )          
    """)
    
    connection.commit()
    connection.close()