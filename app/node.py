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
        if len(CHAIN) == 0:
            CHAIN.append(Block())
        # TODO sync transactions and chain from other nodes
        # try using grpc https://grpc.io/docs/languages/python/basics/

    def mine_block(self):
        self.sync_node()
        new_block = Block(**{
            'data': {'transactions': list(_TRANSACTIONS.values())},
            'nonce': run_proof_of_work(CHAIN[-1]),
        })

        CHAIN.append(new_block)
        _TRANSACTIONS.clear()

        return new_block


def run_proof_of_work(previous_block_hash):
    nonce = 0

    while not validate_nonce(previous_block_hash, nonce):
        nonce += 1

    return nonce


def validate_nonce(previous_block_hash, nonce):
    difficulty = 4
    guess = (f'{previous_block_hash}{nonce}').encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash.startswith('0' * difficulty)
