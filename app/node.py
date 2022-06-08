import jwt

from app.block import CHAIN, Block
from app.config import ALGORITHM
from app.transaction import Transaction


class Node:
    _transactions = dict()

    def __init__(self):
        self.sync()
        pass

    def submit_transaction(self, transaction: Transaction):
        jwt.decode(transaction.sign, transaction.sender_public_key,
                   algorithms=[ALGORITHM])

        self._transactions.update({transaction.sign: transaction})

    @property
    def transactions(self):
        return self._transactions.values()

    def sync(self):
        if len(CHAIN) == 0:
            CHAIN.append(Block())
        # TODO sync transactions and chain from other nodes
        # try using grpc https://grpc.io/docs/languages/python/basics/

    def mine_block(self):
        self.sync()
        new_block = Block({'transactions': list(self._transactions.values())})

        CHAIN.append(new_block)
        self._transactions.clear()

        return new_block

    def to_dict(self):
        return {
            'transactions': [trx.to_dict() for trx in self.transactions]
        }


node = Node()
