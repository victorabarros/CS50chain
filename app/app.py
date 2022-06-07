import json

from block import CHAIN
from transaction import Transaction
from wallet import Wallet
from node import Node


if __name__ == "__main__":
    sender_wallet = Wallet()
    recipient_wallet = Wallet()

    node = Node()

    trx = Transaction(sender_wallet.public_key,
                      recipient_wallet.public_key, 50.2)
    trx.do_sign(sender_wallet.private_key)
    node.submit_transaction(trx)

    # print(CHAIN)
    # print(node.get_transactions())
    node.mine_block()
    print([json.dumps(c.to_dict()) for c in CHAIN])

    # import pdb
    # pdb.set_trace()
