from datetime import datetime
from Crypto.PublicKey import RSA

from app.config import BITS, UNIVERSAL_PRIVATE_KEY, UNIVERSAL_PUBLIC_KEY
from app.block import CHAIN
from app.node import node
from app.transaction import Transaction


class Wallet:
    initial_balance = 1000

    def __init__(self, public_key, private_key):
        self.created_at = datetime.utcnow()
        self._public_key = public_key
        self._private_key = private_key

        self._set_initial_balance()

    def _set_initial_balance(self):
        trx = Transaction(UNIVERSAL_PUBLIC_KEY, self.public_key,
                          self.initial_balance, "Initial balance")

        trx.do_sign(UNIVERSAL_PRIVATE_KEY)

        node.submit_transaction(trx)

    @property
    def balance(self):
        withdraw = 0
        deposit = 0
        for block in CHAIN:
            transactions = block.data.get("transactions", [])
            for trx in transactions:
                if trx.sender_pub_key == self.public_key:
                    withdraw += trx.amount
                if trx.recipient_pub_key == self.public_key:
                    deposit += trx.amount

        return deposit - withdraw

    @property
    def public_key(self):
        return self._public_key

    @property
    def private_key(self):
        return self._private_key

    def to_dict(self):
        return {
            "created_at": self.created_at.isoformat(),
            "public_key": self.public_key,
            "private_key": self.private_key,
        }


def generate_pair_key():
    rsa = RSA.generate(BITS)
    return {
        "private_key": rsa.export_key().decode(),
        "public_key": rsa.publickey().export_key().decode(),
    }


def create_new_wallet():
    return Wallet(**generate_pair_key())
