from datetime import datetime
from Crypto.PublicKey import RSA

from app.config import BITS, INITIAL_BALANCE, UNIVERSAL_PRIVATE_KEY, UNIVERSAL_PUBLIC_KEY
from app.block import CHAIN
from app.node import node
from app.transaction import Transaction


class Wallet:

    def __init__(self, public_key, private_key=None):
        self.created_at = datetime.utcnow()
        self._public_key = public_key.replace("\\n", "\n")
        if (private_key):
            self._private_key = private_key.replace("\\n", "\n")

    @property
    def financial_data(self):
        statement = list()
        withdraw = 0
        deposit = 0
        for block in CHAIN:
            transactions = block.data.get("transactions", [])
            for transaction in transactions:
                if transaction.sender_pub_key == self.public_key:
                    withdraw += transaction.amount
                    statement.append(transaction.to_dict())
                if transaction.recipient_pub_key == self.public_key:
                    deposit += transaction.amount
                    statement.append(transaction.to_dict())

        pending_transactions = \
            filter(lambda transaction:
                   self.public_key in (
                       transaction.sender_pub_key, transaction.recipient_pub_key),
                   node.transactions)
        return {"balance": deposit - withdraw, "statement": statement,
                "pending": list(trx.to_dict() for trx in pending_transactions)}

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


def _set_initial_balance(wallet):
    trx = Transaction(UNIVERSAL_PUBLIC_KEY, wallet.public_key,
                      INITIAL_BALANCE, "Initial balance")

    trx.do_sign(UNIVERSAL_PRIVATE_KEY)

    node.submit_transaction(trx)


def create_new_wallet():
    wallet = Wallet(**generate_pair_key())
    _set_initial_balance(wallet)
    return wallet
