import sqlite3

def init_db(db_name="leds.db"):
    conn = sqlite3.connect(db_name)
    conn.execute("PRAGMA foreign_keys = ON")  # enable cascading deletes
    cursor = conn.cursor()

    # Config table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Config (
        cid INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT
    );
    """)

    # Animation table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Animation (
        aid INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        length INTEGER,
        type TEXT
    );
    """)

    # Relation table (links Config <-> Animation)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Relation (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cid INTEGER NOT NULL,
        aid INTEGER NOT NULL,
        start INTEGER,
        FOREIGN KEY (cid) REFERENCES Config(cid) ON DELETE CASCADE,
        FOREIGN KEY (aid) REFERENCES Animation(aid) ON DELETE CASCADE
    );
    """)

    # Parameter table (key-value with typed columns)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Parameter (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        animation_id INTEGER NOT NULL,
        key TEXT NOT NULL,
        type TEXT NOT NULL,
        int_value INTEGER,
        float_value REAL,
        text_value TEXT,
        bool_value INTEGER, -- use 0/1 for false/true
        FOREIGN KEY (animation_id) REFERENCES Animation(aid)
    );
    """)

    conn.commit()
    conn.close()
    print(f"Database '{db_name}' initialized successfully.")
