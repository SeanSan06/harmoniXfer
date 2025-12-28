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
            id_field INTEGER PRIMARY KEY CHECK (id_field = 1),
            total_songs_transferred_field INTEGER NOT NULL DEFAULT 0,
            total_playlists_transferred_field INTEGER NOT NULL DEFAULT 0,
            total_time_saved_field REAL NOT NULL DEFAULT 0,
            avg_time_per_song_field REAL NOT NULL DEFAULT 0
        )          
    """)
    
    connection.commit()
    connection.close()

def set_table_id():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO statistics (id_field) VALUES (1)
    """)
    
    connection.commit()
    connection.close()