import hashlib
import jwt
from datetime import datetime
import json

from config import ALGORITHM
from transaction import Transaction

_TRANSACTIONS = dict()
_CHAIN = list()


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
        if len(_CHAIN) == 0:
            _CHAIN.append({
                'id': len(_CHAIN),
                'created_at': datetime.utcnow(),
                'data': None,
                'nonce': None,
                'hash': None,
            })
        # TODO sync transactions and chain from other nodes
        # try using grpc https://grpc.io/docs/languages/python/basics/

    def get_chain(self):
        return _CHAIN

    def mine_block(self):
        # self.sync_node()
        new_block = {
            'id': len(_CHAIN),
            'created_at': datetime.utcnow(),
            'data': {'transactions': list(_TRANSACTIONS.values())},
            'nonce': self.proof_of_work(),
            'hash': None,
        }

        new_block['hash'] = hashlib.sha256(json.dumps(
            new_block, sort_keys=True, default=str).encode()).hexdigest()

        _CHAIN.append(new_block)
        _TRANSACTIONS.clear()

        return new_block

    def proof_of_work(self):
        difficulty = 4
        nonce = 0
        previous_block_hash = _CHAIN[-1]['hash']

        while True:
            guess = (f'{previous_block_hash}{nonce}').encode()
            guess_hash = hashlib.sha256(guess).hexdigest()
            if guess_hash.startswith('0' * difficulty):
                break
            nonce += 1

        return nonce
