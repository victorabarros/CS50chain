from datetime import datetime
from Crypto.PublicKey import RSA

from app.config import BITS, INITIAL_BALANCE, UNIVERSAL_PRIVATE_KEY, UNIVERSAL_PUBLIC_KEY
from app.block import CHAIN
from app.node import NODE
from app.transaction import Transaction


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

    NODE.submit_transaction(trx)


class Wallet:

    def __init__(self, public_key, private_key=None):
        self.created_at = datetime.utcnow()
        self._public_key = public_key.replace("\\n", "\n")
        if (private_key):
            self._private_key = private_key.replace("\\n", "\n")

    @property
    def financial_data(self):
        return {
            "balance": self._balance(),
            "statement": self._statement(),
            "pending": self._node_transactions(),
        }

    def _balance(self):
        withdraw = 0
        deposit = 0
        for block in CHAIN.values():
            transactions = block.data.get("transactions", [])
            for transaction in transactions:
                if transaction.sender_public_key == self.public_key:
                    withdraw += transaction.amount
                if transaction.recipient_public_key == self.public_key:
                    deposit += transaction.amount
        return deposit - withdraw

    def _statement(self):
        statement = list()
        for block in CHAIN.values():
            block_transactions = block.data.get("transactions", [])
            statement.extend(list(
                filter(
                    lambda transaction:
                        self.public_key in (
                            transaction.sender_public_key, transaction.recipient_public_key),
                        block_transactions
                )
            ))

        return list(trx.to_dict() for trx in statement)

    def _node_transactions(self):
        pending_transactions = \
            filter(lambda transaction:
                   self.public_key in (
                       transaction.sender_public_key, transaction.recipient_public_key),
                   NODE.transactions)

        return list(trx.to_dict() for trx in pending_transactions)

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

    @staticmethod
    def new():
        wallet = Wallet(**generate_pair_key())
        _set_initial_balance(wallet)
        return wallet
