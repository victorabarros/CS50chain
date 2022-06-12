from cs50 import SQL

from app.config import DATABASE_URL


class Database:
    _db = None

    def __init__(self, database_url=DATABASE_URL):
        try:
            self._db = SQL(database_url)
        except Exception:
            print("The database could not be instantiated")

    def execute(self, *args, **kwargs):
        if self._db is None:
            print("Blockchain data will not be persisted")
            return []

        return DB.execute(*args, **kwargs)


DB = Database()
