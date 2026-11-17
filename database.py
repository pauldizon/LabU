
import sqlite3
import sys
import os
from pathlib import Path

import shutil

if getattr(sys, "frozen", False):
    APP_DIR = Path(os.environ["LOCALAPPDATA"]) / "LabU"
    APP_DIR.mkdir(parents=True, exist_ok=True)

    DATABASE_PATH = APP_DIR / "labu.db"
    BUNDLED_DATABASE = Path(sys._MEIPASS) / "labu.db"

    if not DATABASE_PATH.exists() and BUNDLED_DATABASE.exists():
        shutil.copy2(BUNDLED_DATABASE, DATABASE_PATH)

else:
    APP_DIR = Path(__file__).resolve().parent
    DATABASE_PATH = APP_DIR / "labu.db"

def get_connection():
    """Create a connection to the SQLite database."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    """Create the component inventory table if it doesn't exist."""

    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS components (
                component_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 0
                    CHECK(quantity >= 0),
                location TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create the transaction history table.
        # This preserves records of inventory activities.
        connection.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                component_id TEXT NOT NULL,
                component_name TEXT NOT NULL,
                action TEXT NOT NULL,
                details TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


        connection.commit()


def add_component(component_id, name, category, quantity, location):
    """Insert a new component into the inventory."""

    with get_connection() as connection:
        connection.execute("""
            INSERT INTO components
            (component_id, name, category, quantity, location)
            VALUES (?, ?, ?, ?, ?)
        """, (component_id, name, category, quantity, location))


def get_all_components():
    """Retrieve all inventory records."""

    with get_connection() as connection:
        records = connection.execute("""
            SELECT * FROM components
            ORDER BY name ASC
        """).fetchall()

        return [dict(record) for record in records]


def update_component(component_id, name, category, quantity, location):
    """Update an existing component."""

    with get_connection() as connection:
        cursor = connection.execute("""
            UPDATE components
            SET name = ?,
                category = ?,
                quantity = ?,
                location = ?
            WHERE component_id = ?
        """, (name, category, quantity, location, component_id))

        return cursor.rowcount > 0


def delete_component(component_id):
    """Delete a component from the inventory."""

    with get_connection() as connection:
        cursor = connection.execute("""
            DELETE FROM components
            WHERE component_id = ?
        """, (component_id,))

        return cursor.rowcount > 0


def search_components(keyword):
    """Search components by ID or name."""

    with get_connection() as connection:
        records = connection.execute("""
            SELECT * FROM components
            WHERE component_id LIKE ?
               OR name LIKE ?
            ORDER BY name ASC
        """, (f"%{keyword}%", f"%{keyword}%")).fetchall()

        return [dict(record) for record in records]
    
    
# ==========================================
# TRANSACTION HISTORY FUNCTIONS
# ==========================================

def log_transaction(component_id, component_name, action, details=""):
    """
    Record an inventory activity.
    Actions include ADD, UPDATE, and DELETE.
    """

    with get_connection() as connection:
        connection.execute("""
            INSERT INTO transactions
            (component_id, component_name, action, details)
            VALUES (?, ?, ?, ?)
        """, (component_id, component_name, action, details))


def get_all_transactions():
    """Retrieve all transactions, newest first."""

    with get_connection() as connection:
        records = connection.execute("""
            SELECT * FROM transactions
            ORDER BY transaction_id DESC
        """).fetchall()

        return [dict(record) for record in records]

    # TRANSACTION HISTORY FUNCTIONS
def log_transaction(component_id, component_name, action, details=""):
    """
    Record an inventory activity.
    Actions include ADD, UPDATE, and DELETE.
    """

    with get_connection() as connection:
        connection.execute("""
            INSERT INTO transactions
            (component_id, component_name, action, details)
            VALUES (?, ?, ?, ?)
        """, (component_id, component_name, action, details))


def get_all_transactions():
    """Retrieve all transactions, newest first."""

    with get_connection() as connection:
        records = connection.execute("""
            SELECT * FROM transactions
            ORDER BY transaction_id DESC
        """).fetchall()

        return [dict(record) for record in records]


def search_transactions(keyword):
    """Search by component ID, name, or action."""

    with get_connection() as connection:
        records = connection.execute("""
            SELECT * FROM transactions
            WHERE component_id LIKE ?
               OR component_name LIKE ?
               OR action LIKE ?
            ORDER BY transaction_id DESC
        """, (
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%"
        )).fetchall()

        return [dict(record) for record in records]

