import sqlite3
from typing import List, Tuple
from datetime import datetime

class DatabaseManager:
    """Administra la persistencia del historial en SQLite."""

    def __init__(self, db_name: str = "historial.db") -> None:
        self.db_name = db_name
        self._create_table()

    def _create_table(self) -> None:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operation TEXT NOT NULL,
                    result REAL NOT NULL,
                    timestamp TEXT NOT NULL
                )
            """)
            conn.commit()

    def save_operation(self, operation: str, result: float) -> None:
        """Guarda una operación realizada en la base de datos."""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO history (operation, result, timestamp) VALUES (?, ?, ?)",
                (operation, result, now)
            )
            conn.commit()

    def get_history(self) -> List[Tuple[int, str, float, str]]:
        """Recupera todas las operaciones guardadas."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, operation, result, timestamp FROM history ORDER BY id DESC")
            return cursor.fetchall()
