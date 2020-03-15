import os
import sqlite3


class Restaurant:
    _db = None

    @classmethod
    def _get_database(cls) -> sqlite3.Connection:
        cls._db = sqlite3.connect(os.path.join(os.getcwd(), "restaurant.db"))
        cursor = cls._db.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS restaurant(\
                id INTEGER PRIMARY KEY AUTOINCREMENT, \
                name TEXT UNIQUE NOT NULL, \
                info TEXT NOT NULL, \
                address TEXT NOT NULL, \
                link TEXT NOT NULL \
            );"
        )
        return cls._db

    def select_all(self) -> sqlite3.Cursor:
        db = self._get_database()
        cursor = db.cursor()
        return cursor.execute("SELECT * FROM restaurant")

    def select_by_name(self, name: str = "") -> sqlite3.Cursor:
        db = self._get_database()
        cursor = db.cursor()
        return cursor.execute("SELECT * FROM restaurant WHERE name LIKE ?", ("%" + name + "%",))

    def select_by_info(self, info: str = "") -> sqlite3.Cursor:
        db = self._get_database()
        cursor = db.cursor()
        return cursor.execute("SELECT * FROM restaurant WHERE info LIKE ?", ("%" + info + "%",))
