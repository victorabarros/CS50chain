import hashlib
import json
from datetime import datetime

from app.config import NONCE_VALIDATION_DIFFICULTY


CHAIN = list()


class Block:
    _hash = None
    _nonce = None

    def __init__(self, data={}):
        self.id = len(CHAIN)
        self.created_at = datetime.utcnow()
        self._data = data
        if len(CHAIN) > 0:
            self._nonce = run_proof_of_work(CHAIN[-1].hash)

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


def run_proof_of_work(previous_block_hash):
    nonce = 0

    while not validate_nonce(previous_block_hash, nonce):
        nonce += 1

    return nonce


def validate_nonce(previous_block_hash, nonce):
    guess = (f'{previous_block_hash}{nonce}').encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash.startswith('0' * NONCE_VALIDATION_DIFFICULTY)
