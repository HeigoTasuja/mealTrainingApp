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
        c.execute("""
            CREATE TABLE IF NOT EXISTS workouts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                session_type TEXT,
                body_part TEXT,
                exercises TEXT,
                notes TEXT
            )
        """)

        # Meals table (logged meals)
        c.execute("""
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
        """)

        # Workout plans table (plans UI)
        c.execute("""
            CREATE TABLE IF NOT EXISTS workout_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                category TEXT,
                day TEXT,         -- e.g., Monday, Tuesday...
                type TEXT,        -- e.g., mobility or strength
                body_part TEXT
            )
        """)

        # Exercises linked to workout plans
        c.execute("""
            CREATE TABLE IF NOT EXISTS exercises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                day TEXT NOT NULL,
                category TEXT NOT NULL
            )
        """)

        # Meal plans table (planner UI)
        c.execute("""
            CREATE TABLE IF NOT EXISTS meal_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                day TEXT NOT NULL,
                meal_type TEXT NOT NULL,
                name TEXT NOT NULL,
                ingredients TEXT,
                calories REAL
            )
        """)

        # Ingredients reference table
        c.execute("""
            CREATE TABLE IF NOT EXISTS ingredients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                calories REAL NOT NULL,
                protein REAL NOT NULL,
                carbs REAL NOT NULL,
                fat REAL NOT NULL
            )
        """)

        # Meal ingredients link table (for meal_plans)
        c.execute("""
            CREATE TABLE IF NOT EXISTS meal_ingredients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                meal_id INTEGER NOT NULL,
                ingredient_id INTEGER NOT NULL,
                grams REAL NOT NULL,
                FOREIGN KEY(meal_id) REFERENCES meal_plans(id),
                FOREIGN KEY(ingredient_id) REFERENCES ingredients(id)
            )
        """)

        conn.commit()
