import jwt
import json
import requests
from typing import Dict

from app.block import Block, CHAIN
from app.config import ALGORITHM
from app.transaction import Transaction


class Node:
    _transactions: Dict[str, Transaction] = dict()
    _nodes = set()

    @property
    def transactions(self):
        return list(self._transactions.values())

    @property
    def nodes(self):
        return self._nodes

    def submit_transaction(self, transaction: Transaction):
        jwt.decode(transaction.sign, transaction.sender_public_key,
                   algorithms=[ALGORITHM])

        self._transactions.update({transaction.sign: transaction})

    def add_node_address(self, address):
        # IMPROVE check if url is valid; use regex
        self._nodes.add(address)

    def sync(self):
        # IMPROVE grpc https://grpc.io/docs/languages/python/basics/
        self._sync_transactions()
        self.sync_blockchain()

    def _sync_transactions(self):
        new_nodes = set()
        # IMPROVE do asynchronously/parallel https://docs.python.org/3/library/asyncio-task.html
        for address in list(self._nodes):
            try:
                resp = requests.get(f"{address}/api/node")
                if not resp.ok:
                    continue
                payload = resp.json()

                for transaction in payload["transactions"]:
                    trx = Transaction.from_dict(**transaction)
                    self._transactions.update({trx.sign: trx})

                new_nodes.update(payload["nodes"])

                # IMPROVE do asynchronously and don't need wait response
                requests.delete(f"{address}/api/node/transactions")
            except Exception as e:
                print(e)
                continue
        self._nodes.update(new_nodes)

    def sync_blockchain(self):
        # IMPROVE do asynchronously/parallel https://docs.python.org/3/library/asyncio-task.html
        for address in self._nodes:
            try:
                resp = requests.get(f"{address}/api/chain")
                if not resp.ok:
                    continue
            except Exception as e:
                print(e)
                continue
            payload = resp.json()
            for block in payload:
                block = Block.from_dict(**block)

                CHAIN.update({block.id: block})

    def mine_block(self):
        self.sync()
        new_block = Block({"transactions": list(self._transactions.values())})
        CHAIN.update({new_block.id: new_block})

        self.clear_transactions()

        # IMPROVE do asynchronously, don't need wait answer https://docs.python.org/3/library/asyncio-task.html
        for address in self._nodes:
            try:
                requests.post(f"{address}/api/chain")
            except Exception as e:
                print(e)
                continue

        new_block_dict = new_block.to_dict()
        new_block_dict["data"] = json.dumps(new_block_dict["data"])

        return new_block

    def clear_transactions(self):
        self._transactions.clear()

    def to_dict(self):
        return {
            "transactions": [trx.to_dict() for trx in self.transactions],
            "nodes": list(self._nodes)
        }

    @staticmethod
    def from_dict(**kwargs):
        n = Node()

        [n.add_node_address(address) for address in kwargs["nodes"]]
        [n.submit_transaction(Transaction.from_dict(**trx))
         for trx in kwargs["transactions"]]

        return n


NODE = Node()
