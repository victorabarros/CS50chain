import hashlib
import json
from datetime import datetime
from typing import Dict

from app.config import DATABASE_URL, NONCE_VALIDATION_DIFFICULTY
from app.database import DB
from app.transaction import Transaction


class Block:
    _id = None
    _created_at = None
    _data = None
    _nonce = None
    _hash = None

    def __init__(self, data={}):
        blockchain_len = len(CHAIN)
        self._id = blockchain_len
        self._created_at = datetime.utcnow()
        self._data = data
        if blockchain_len > 0:
            self._nonce = run_proof_of_work(CHAIN[blockchain_len-1].hash)

    def _internal_to_dict(self):
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "data": {**self._data, "transactions": [trx.to_dict() for trx in self._data.get("transactions", [])]},
            "nonce": self._nonce,
        }

    def to_dict(self):
        return {**self._internal_to_dict(), "hash": self.hash}

    @staticmethod
    def from_dict(**kwargs):
        kwargs["created_at"] = datetime.fromisoformat(kwargs["created_at"])

        if (kwargs["data"].get("transactions")):
            kwargs["data"]["transactions"] = [Transaction.from_dict(
                **trx) for trx in kwargs["data"]["transactions"]]

        b = Block()
        b._id = kwargs["id"]
        b._created_at = kwargs["created_at"]
        b._hash = kwargs["hash"]
        b._nonce = kwargs["nonce"]
        b._data = kwargs["data"]
        return b

    @property
    def hash(self):
        if self._hash:
            return self._hash
        dumped = json.dumps({**self._internal_to_dict(), "hash": None},
                            sort_keys=True, default=str)
        self._hash = hashlib.sha256(dumped.encode()).hexdigest()
        return self._hash

    @property
    def id(self):
        return self._id

    @property
    def created_at(self):
        return self._created_at

    @property
    def data(self):
        return self._data

    @property
    def nonce(self):
        return self._nonce


def run_proof_of_work(previous_block_hash):
    nonce = 0

    while not validate_nonce(previous_block_hash, nonce):
        nonce += 1

    return nonce


def validate_nonce(previous_block_hash, nonce):
    guess = (f"{previous_block_hash}{nonce}").encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash.startswith("0" * NONCE_VALIDATION_DIFFICULTY)


class Blockchain:
    _chain: Dict[int, Block] = dict()

    def __getitem__(self, item):
        return self._chain[item]

    def __len__(self):
        return len(self._chain)

    def values(self):
        return self._chain.values()

    def update(self, id_block):
        for block in id_block.values():
            row = block.to_dict()
            row["data"] = json.dumps(row["data"])
            # IMPROVE insert asynchronously
            DB.execute("INSERT INTO blockchain (id, data, hash, nonce, created_at) VALUES(?, ?, ?, ?, ?)",
                       row["id"], row["data"], row["hash"], row["nonce"], row["created_at"])

        return self._chain.update(id_block)

    @classmethod
    def load_chain(cls):
        rows = DB.execute("select * from blockchain")
        for block in rows:
            block["data"] = json.loads(block["data"])
            cls._chain.update({block["id"]: Block.from_dict(**block)})


CHAIN = Blockchain()
