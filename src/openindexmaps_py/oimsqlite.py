import sqlite3


def initialize_database(db_path):
    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()

        # Create openindexmaps table
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS openindexmaps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            json_data TEXT,
            metadata TEXT,
            defaults TEXT
        )
        """
        )

        # Create sheets table
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS sheets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            openindexmap_id INTEGER,
            json_data TEXT,
            FOREIGN KEY (openindexmap_id) REFERENCES openindexmaps(id)
        )
        """
        )


def insert_openindexmap(db_path, name, json_data, metadata, defaults):
    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
        INSERT INTO openindexmaps (name, json_data, metadata, defaults)
        VALUES (?, ?, ?, ?)
        """,
            (name, json_data, metadata, defaults),
        )


def delete_openindexmap(db_path, name):
    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM openindexmaps WHERE name = ?", (name,))
