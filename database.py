import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "data.db"


def get_connection():
    """Return a sqlite connection with row access by column name."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create tables if they do not exist (idempotent)."""
    with get_connection() as conn:
        c = conn.cursor()
        # Workouts table
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS workouts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                session_type TEXT,
                body_part TEXT,
                exercises TEXT,
                notes TEXT
            )
            """
        )
        # Meals table
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS meals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                meal_time TEXT,
                description TEXT,
                protein REAL,
                carbs REAL,
                fat REAL,
                fasted TEXT
            )
            """
        )
        # New tables for workout plans and exercises
        c.execute("""
            CREATE TABLE IF NOT EXISTS workout_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                category TEXT  -- 'mobility' or 'strength'
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS exercises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plan_id INTEGER,
                name TEXT,
                description TEXT,
                FOREIGN KEY(plan_id) REFERENCES workout_plans(id) ON DELETE CASCADE
            )
        """)
        conn.commit()

