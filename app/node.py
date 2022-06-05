from transaction import Transaction

_TRANSACTIONS = dict()


class Node:

    def __init__(self):
        # TODO sync transactions and chain from other nodes
        pass

    @staticmethod
    def submit_transaction(transaction: Transaction):
        if (not transaction.sign):
            # TODO raise exception
            pass

        _TRANSACTIONS.update({
            transaction.sign: transaction
        })

    def get_transactions(self):
        return _TRANSACTIONS.values()
