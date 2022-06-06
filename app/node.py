import jwt

from config import ALGORITHM
from transaction import Transaction

_TRANSACTIONS = dict()


class Node:

    def __init__(self):
        self.sync_node()
        pass

    @staticmethod
    def submit_transaction(transaction: Transaction):
        if (not transaction.sign):
            # TODO raise exception
            pass

        jwt.decode(transaction.sign, transaction.sender_pub_key,
                   algorithms=[ALGORITHM])

        _TRANSACTIONS.update({
            transaction.sign: transaction
        })

    def get_transactions(self):
        return _TRANSACTIONS.values()

    def sync_node(self):
        # TODO sync transactions and chain from other nodes
        # try using grpc https://grpc.io/docs/languages/python/basics/
        pass
