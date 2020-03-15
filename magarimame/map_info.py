import os
import sqlite3
from typing import Dict, Optional, Tuple


class MapInfo:
    _db = None

    @classmethod
    def _get_database(cls) -> sqlite3.Connection:
        cls._db = sqlite3.connect(os.path.join(os.getcwd(), "mapinfo.db"))
        cursor = cls._db.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS mapinfo(\
                id INTEGER PRIMARY KEY AUTOINCREMENT, \
                name TEXT UNIQUE NOT NULL, \
                lat TEXT NOT NULL, \
                lon TEXT NOT NULL, \
                link TEXT NOT NULL \
            );"
        )
        return cls._db

    def is_already_exist(self, name: str) -> bool:
        if self._find_mapinfo(name):
            return True
        else:
            return False

    def _find_mapinfo(self, name: str) -> Optional[Tuple]:
        db = self._get_database()
        cursor = db.execute("SELECT * FROM mapinfo WHERE name=?", (name,))
        return cursor.fetchone()

    def save(self, item: Dict):
        if self._find_mapinfo(item["name"]):
            return

        db = self._get_database()
        db.execute(
            "INSERT INTO mapinfo (name, lat, lon, link) VALUES (?, ?, ?, ?)",
            (item["name"], item["lat"], item["lon"], item["link"],),
        )
        db.commit()

    def select_all(self) -> sqlite3.Cursor:
        db = self._get_database()
        cursor = db.cursor()
        return cursor.execute("SELECT * FROM mapinfo")

    def select_by_name(self, name: str) -> sqlite3.Cursor:
        db = self._get_database()
        cursor = db.cursor()
        return cursor.execute("SELECT * FROM mapinfo WHERE name LIKE ?", ("%" + name + "%",))
