import os
import sqlite3


class RestaurantScrapyPipeline(object):
    _db = None

    @classmethod
    def get_database(cls):
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

    def process_item(self, item, spider):
        self.save_post(item)
        return item

    def save_post(self, item):
        if self.find_post(item["name"]):
            return

        db = self.get_database()
        db.execute(
            "INSERT INTO restaurant (name, info, address, link) VALUES (?, ?, ?, ?)",
            (item["name"], item["info"], item["address"], item["link"],),
        )
        db.commit()

    def find_post(self, name):
        db = self.get_database()
        cursor = db.execute("SELECT * FROM restaurant WHERE name=?", (name,))
        return cursor.fetchone()
