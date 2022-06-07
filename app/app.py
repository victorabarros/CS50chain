import jwt
import json

from config import ALGORITHM
from block import CHAIN, Block, validate_nonce
from transaction import Transaction
from wallet import Wallet
from node import node, Node

if __name__ == "__main__":
    CHAIN.append(Block())
    victor = Wallet()
    vanessa = Wallet()

    node.mine_block()

    trx1 = Transaction(victor.public_key,
                       vanessa.public_key, 70.2, "valentines dinner")
    trx1.do_sign(victor.private_key)

    node.submit_transaction(trx1)
    node.mine_block()

    trx2 = Transaction(vanessa.public_key,
                       victor.public_key, 2.09, "cookie")
    trx2.do_sign(vanessa.private_key)
    node.submit_transaction(trx2)
    node.mine_block()

    for block in CHAIN:
        print(json.dumps(block.to_dict()))
        if block.id == 0:
            continue
        previous_block_hash = CHAIN[block.id-1].hash
        if not validate_nonce(previous_block_hash, block.nonce):
            raise Exception("nonce invalid")
        for trx in block.data.get("transactions", []):
            jwt.decode(trx.sign, trx.sender_pub_key,
                       algorithms=[ALGORITHM])

    print(victor.balance, vanessa.balance)
    # import pdb
    # pdb.set_trace()
