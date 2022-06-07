from transaction import Transaction
from wallet import Wallet
from node import Node


if __name__ == "__main__":
    sender_wallet = Wallet()
    print("sender done")
    recipient_wallet = Wallet()
    print("recipient done")

    node = Node()

    # trx = Transaction(sender_wallet.public_key,
    #                   recipient_wallet.public_key, 50.2)
    # trx.do_sign(sender_wallet.private_key)
    # node.submit_transaction(trx)

    print(node.get_chain())
    print(node.get_transactions())
    node.mine_block()
    print(node.get_chain())
    print(node.get_transactions())

    # import pdb; pdb.set_trace()
