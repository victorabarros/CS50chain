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
        self._nodes.add("http://172.17.0.4:5000")
        self._nodes.add("http://172.17.0.5:5000")
        self._nodes.add("http://172.17.0.6:5000")
        self._nodes.add("http://172.17.0.7:5000")

    def submit_transaction(self, transaction: Transaction):
        jwt.decode(transaction.sign, transaction.sender_public_key,
                   algorithms=[ALGORITHM])

        self._transactions.update({transaction.sign: transaction})

    @property
    def transactions(self):
        return self._transactions.values()

    def sync(self):
        self._sync_transactions()
        self.sync_blockchain()
        # IMPROVE grpc https://grpc.io/docs/languages/python/basics/

        if len(CHAIN) == 0:
            CHAIN.update({0: Block()})
            return

    def _sync_transactions(self):
        new_nodes = set()
        for address in self._nodes:
            resp = requests.get(f"{address}/api/node")
            if not resp.ok:
                continue
            payload = resp.json()
            node = Node.from_dict(**payload)

            self._transactions.update(node._transactions)
            new_nodes.update(node._nodes)
            # IMPROVE do asynchronously
            requests.delete(f"{address}/api/node/transactions")
        self._nodes.update(new_nodes)

    def sync_blockchain(self):
        for address in self._nodes:
            resp = requests.get(f"{address}/api/chain")
            if not resp.ok:
                continue
            payload = resp.json()
            for block in payload:
                block = Block.from_dict(**block)

                CHAIN.update({block.id: block})

    def mine_block(self):
        self.sync()
        new_block = Block({'transactions': list(self._transactions.values())})
        self.clear_transactions()

        CHAIN.update({new_block.id: new_block})

        # IMPROVE do asynchronously
        [requests.post(f"{address}/api/chain") for address in self._nodes]

        new_block_dict = new_block.to_dict()
        new_block_dict["data"] = json.dumps(new_block_dict["data"])

        return new_block

    def clear_transactions(self):
        self._transactions.clear()

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

    def add_node_address(self, address):
        # IMPROVE check if url is valid; use regex
        self._nodes.add(address)


node = Node()
