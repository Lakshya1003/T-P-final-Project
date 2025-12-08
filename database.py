import sqlite3
import os

DB_NAME = "blueberry_commands.db"

def init_db():
    """Initialize the database with the commands table."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS commands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            command_phrase TEXT UNIQUE NOT NULL,
            action_type TEXT NOT NULL,
            action_value TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_command(phrase, action_type, action_value):
    """Add a new custom command."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO commands (command_phrase, action_type, action_value) VALUES (?, ?, ?)",
            (phrase.lower(), action_type, action_value)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding command: {e}")
        return False

def get_command(phrase):
    """Retrieve a command by its phrase."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT action_type, action_value FROM commands WHERE command_phrase = ?", (phrase.lower(),))
    result = cursor.fetchone()
    conn.close()
    return result

def get_all_commands():
    """Get all custom commands."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT command_phrase, action_type, action_value FROM commands")
    results = cursor.fetchall()
    conn.close()
    return results

# Initialize DB on module load
init_db()
