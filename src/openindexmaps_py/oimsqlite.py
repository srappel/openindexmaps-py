import sqlite3


def initialize_database(db_path):
    connection = sqlite3.connect(db_path)
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

    connection.commit()
    connection.close()


def insert_openindexmap(db_path, name, json_data, metadata, defaults):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute(
        """
    INSERT INTO openindexmaps (name, json_data, metadata, defaults)
    VALUES (?, ?, ?, ?)
    """,
        (name, json_data, metadata, defaults),
    )

    connection.commit()
    connection.close()


def delete_openindexmap(db_path, name):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("DELETE FROM openindexmaps WHERE name = ?", (name,))

    connection.commit()
    connection.close()


if __name__ == "__main__":
    initialize_database("db/datastore.db")
    # INSERT INTO openindexmaps (name, json_data, metadata, defaults)
    insert_openindexmap(
        "db/datastore.db",
        "Test OIM",
        '{"type": "FeatureCollection"}',
        '{"id": "500"}',
        '{"publsiher": "Default Publishing House"}',
    )
    # DELETE FROM openindexmaps WHERE name = ?
    delete_openindexmap("db/datastore.db", "Test OIM")
