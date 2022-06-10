import jwt
import json

import requests

from app.block import CHAIN, Block
from app.config import ALGORITHM
from app.transaction import Transaction


class Node:
    _transactions = dict()
    _nodes = set()

    def __init__(self):
        # self.sync()
        self.add_node_address("http://172.17.0.4:5000")  # todo remove

    def submit_transaction(self, transaction: Transaction):
        jwt.decode(transaction.sign, transaction.sender_public_key,
                   algorithms=[ALGORITHM])

        self._transactions.update({transaction.sign: transaction})

    @property
    def transactions(self):
        return self._transactions.values()

    def sync(self):
        trxs = self._sync_transactions()
        # TODO sync chain with other nodes
        # IMPROVE grpc https://grpc.io/docs/languages/python/basics/

        if len(CHAIN) == 0:
            CHAIN.append(Block())
            return

    def _sync_transactions(self):
        for address in self._nodes:
            resp = requests.get(f"{address}/api/node")
            if not resp.ok:
                return
            payload = resp.json()
            node = Node.from_dict(**payload)
            self._merge(node)

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
            "nodes": list(self._nodes)
        }

    @staticmethod
    def from_dict(**kwargs):
        n = Node()

        [n.add_node_address(address) for address in kwargs["nodes"]]
        [n.submit_transaction(Transaction.from_dict(**trx))
         for trx in kwargs["transactions"]]

        return n

    def _merge(self, node):
        self._nodes.update(node._nodes)
        self._transactions.update(node._transactions)

    def add_node_address(self, address):
        # IMPROVE check if url is valid; use regex
        self._nodes.add(address)


node = Node()
