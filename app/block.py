import hashlib
import json
from datetime import datetime


CHAIN = list()


class Block:
    _hash = None

    def __init__(self, nonce=None, data={}):
        self.id = len(CHAIN)
        self.created_at = datetime.utcnow()
        self._data = data
        self._nonce = nonce

    def _internal_to_dict(self):
        return {
            'id': self.id,
            "created_at": self.created_at.isoformat(),
            'data': {**self._data, 'transactions': [trx.to_dict() for trx in self._data.get('transactions', [])]},
            'nonce': self._nonce,
        }

    def to_dict(self):
        return {**self._internal_to_dict(), 'hash': self.hash}

    @property
    def hash(self):
        if self._hash:
            return self._hash
        dumped = json.dumps({**self._internal_to_dict(), "hash": None},
                            sort_keys=True, default=str)
        self._hash = hashlib.sha256(dumped.encode()).hexdigest()
        return self._hash

    @property
    def data(self):
        return self._data

    @property
    def nonce(self):
        return self._nonce
