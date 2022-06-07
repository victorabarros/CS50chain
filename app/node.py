import hashlib
import jwt

from block import CHAIN, Block
from config import ALGORITHM
from transaction import Transaction

_TRANSACTIONS = dict()


class Node:

    def __init__(self):
        self.sync_node()
        pass

    @staticmethod
    def submit_transaction(transaction: Transaction):
        jwt.decode(transaction.sign, transaction.sender_pub_key,
                   algorithms=[ALGORITHM])

        _TRANSACTIONS.update({transaction.sign: transaction})

    def get_transactions(self):
        return _TRANSACTIONS.values()

    def sync_node(self):
        # TODO sync transactions and chain from other nodes
        # try using grpc https://grpc.io/docs/languages/python/basics/
        pass

    def mine_block(self):
        self.sync_node()
        new_block = Block({'transactions': list(_TRANSACTIONS.values())})

        CHAIN.append(new_block)
        _TRANSACTIONS.clear()

        return new_block
