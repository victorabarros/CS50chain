from cs50 import SQL

from app.config import DATABASE_URL

db = SQL(DATABASE_URL)


class Blockchain:
    _chain = dict()

    def __init__(self):
        # TODO fetch from db
        pass

    def __getitem__(self, item):
        return self._chain[item]

    def __len__(self):
        return len(self._chain)

    def values(self):
        return self._chain.values()

    def update(self, values):
        # TODO add to db
        return self._chain.update(values)


CHAIN = Blockchain()
