import jwt
import json
from datetime import datetime
from cs50 import SQL

from app.block import CHAIN, Block
from app.config import ALGORITHM, DATABASE_URL
from app.transaction import Transaction

db = SQL(DATABASE_URL)


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

    def _sync_chain_with_db(self):
        resp = db.execute("SELECT * FROM blockchain")
        if len(resp) == 0:
            CHAIN.append(Block())
            return

        CHAIN.clear()
        for block in resp:
            # IMPROVE remove clear, iterate reversed and check if block has same hash; break
            block["data"] = json.loads(block["data"])

            CHAIN.append(Block.from_dict(**block))

    def sync(self):
        self._sync_chain_with_db()
        # TODO sync chain with other nodes
        # TODO sync transactions with other nodes
        # IMPROVE grpc https://grpc.io/docs/languages/python/basics/

    def mine_block(self):
        self.sync()
        new_block = Block({'transactions': list(self._transactions.values())})

        CHAIN.append(new_block)

        new_block_dict = new_block.to_dict()
        new_block_dict["data"] = json.dumps(new_block_dict["data"])

        # IMPROVE do async
        db.execute(
            "INSERT INTO blockchain (id, created_at, data, nonce, hash) VALUES(?, ?, ?, ?, ?)",
            *new_block_dict.values())

        self._transactions.clear()

        return new_block

    def to_dict(self):
        return {
            'transactions': [trx.to_dict() for trx in self.transactions]
        }


node = Node()
