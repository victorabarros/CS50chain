import hashlib
from datetime import datetime

from transaction import Transaction


class Wallet:
    initial_balance = 1000

    def __init__(self, pub_key: str):
        self.created_at = datetime.utcnow()
        # TODO improve how create pub and pem key (https://cryptography.io/en/latest/)
        self.public_key = pub_key
        self.private_key = hashlib.sha256(
            f"{self.created_at}{self.public_key}".encode()).hexdigest()
        self._set_initial_balance()

    def _set_initial_balance(self):
        trx = Transaction(self.public_key, self.private_key,
                          self.initial_balance, "Initial balance")
        # TODO send to blockchain
