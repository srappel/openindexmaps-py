import sqlite3


def initialize_database():
    conn = sqlite3.connect("db/datastore.db")
    cursor = conn.cursor()

    # Create tables if they don't already exist
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS openindexmaps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        json_data TEXT
    )
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS sheets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        openindexmap_id INTEGER,
        title TEXT NOT NULL,
        sheet_number INTEGER,
        json_data TEXT,
        FOREIGN KEY (openindexmap_id) REFERENCES openindexmaps(id)
    )
    """
    )

    conn.commit()
    conn.close()
