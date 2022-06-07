from datetime import datetime
from Crypto.PublicKey import RSA

from config import BITS, UNIVERSAL_PRIVATE_KEY, UNIVERSAL_PUBLIC_KEY
from block import CHAIN
from node import Node
from transaction import Transaction


class Wallet:
    initial_balance = 1000

    def __init__(self):
        self.created_at = datetime.utcnow()
        # TODO improve how create pub and pem key (https://cryptography.io/en/latest/)
        rsa = RSA.generate(BITS)

        self.private_key = rsa.export_key().decode()
        self.public_key = rsa.publickey().export_key().decode()

        self._set_initial_balance()

    def _set_initial_balance(self):
        trx = Transaction(UNIVERSAL_PUBLIC_KEY, self.public_key,
                          self.initial_balance, "Initial balance")

        trx.do_sign(UNIVERSAL_PRIVATE_KEY)

        Node.submit_transaction(trx)

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
