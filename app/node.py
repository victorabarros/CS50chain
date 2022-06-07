import hashlib
import jwt

from app.block import CHAIN, Block
from app.config import ALGORITHM
from app.transaction import Transaction


class Node:
    _transactions = dict()

    def __init__(self):
        self.sync_node()
        pass

    def submit_transaction(self, transaction: Transaction):
        jwt.decode(transaction.sign, transaction.sender_pub_key,
                   algorithms=[ALGORITHM])

        self._transactions.update({transaction.sign: transaction})

    @property
    def transactions(self):
        return self._transactions.values()

    def sync_node(self):
        # TODO sync transactions and chain from other nodes
        # try using grpc https://grpc.io/docs/languages/python/basics/
        pass

    def mine_block(self):
        self.sync_node()
        new_block = Block({'transactions': list(self._transactions.values())})

        CHAIN.append(new_block)
        self._transactions.clear()

        return new_block


node = Node()
