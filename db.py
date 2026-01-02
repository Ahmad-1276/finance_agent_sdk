import sqlite3
from typing import Optional, List, Tuple

class Database:
    def __init__(self, db_name: str = "finance.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_tables()
    
    def _create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT,
            note TEXT,
            date TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)
        self.conn.commit()
    
    def add_expense(self, amount: float, category: str = "general", note: str = "") -> str:
        self.cursor.execute(
            "INSERT INTO expenses (amount, category, note) VALUES (?, ?, ?)",
            (amount, category, note)
        )
        self.conn.commit()
        return f"✅ Added expense: ${amount:.2f} for {category}"
    
    def get_total(self) -> float:
        self.cursor.execute("SELECT SUM(amount) FROM expenses")
        total = self.cursor.fetchone()[0] or 0
        return total
    
    def get_average(self) -> float:
        self.cursor.execute("SELECT AVG(amount) FROM expenses")
        avg = self.cursor.fetchone()[0] or 0
        return round(avg, 2) if avg else 0.0
    
    def get_recent_expenses(self, limit: int = 10) -> List[Tuple]:
        self.cursor.execute("SELECT * FROM expenses ORDER BY date DESC LIMIT ?", (limit,))
        return self.cursor.fetchall()
    
    def get_expenses_by_category(self) -> dict:
        self.cursor.execute("""
            SELECT category, COUNT(*), SUM(amount) 
            FROM expenses 
            GROUP BY category 
            ORDER BY SUM(amount) DESC
        """)
        result = {}
        for row in self.cursor.fetchall():
            result[row[0]] = {"count": row[1], "total": row[2] or 0}
        return result
    
    def get_all_expenses(self) -> List[Tuple]:
        self.cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
        return self.cursor.fetchall()
    
    def delete_expense(self, expense_id: int) -> bool:
        try:
            self.cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except:
            return False

# Global instance
db = Database()