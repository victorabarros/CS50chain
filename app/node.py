import jwt
import json

from app.block import CHAIN, Block
from app.config import ALGORITHM
from app.transaction import Transaction


class Node:
    _transactions = dict()
    _nodes = list()

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
            return
        # TODO sync chain with other nodes
        # TODO sync transactions with other nodes
        # IMPROVE grpc https://grpc.io/docs/languages/python/basics/

    def mine_block(self):
        self.sync()
        new_block = Block({'transactions': list(self._transactions.values())})

        CHAIN.append(new_block)

        new_block_dict = new_block.to_dict()
        new_block_dict["data"] = json.dumps(new_block_dict["data"])

        self._transactions.clear()

        return new_block

    def to_dict(self):
        return {
            'transactions': [trx.to_dict() for trx in self.transactions],
            "nodes": self._nodes
        }

    def add_node_address(self, address):
        self._nodes.append(address)


node = Node()
