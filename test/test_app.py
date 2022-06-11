import jwt
import unittest
import json

from app.block import CHAIN, validate_nonce
from app.config import ALGORITHM, INITIAL_BALANCE
from app.transaction import Transaction
from app.node import Node, node
from app.wallet import create_new_wallet, generate_pair_key


class TestNode(unittest.TestCase):
    def test_init_node(self):
        _node = Node()
        self.assertEqual(len(_node._transactions), 0)
        self.assertEqual(len(_node._transactions), len(_node.transactions))
        self.assertEqual(len(_node._nodes), 0)

    def test_submit_transaction(self):
        _node = Node()
        sender = generate_pair_key()
        recipient = generate_pair_key()
        transaction = Transaction(sender["public_key"],
                                  recipient["public_key"], 16.58, "test")

        with self.assertRaises(jwt.exceptions.DecodeError):
            # must fail, because the transaction is not signed
            _node.submit_transaction(transaction)

        transaction_signed = transaction.do_sign(sender["private_key"])
        self.assertEqual(id(transaction_signed), id(transaction))

        _node.submit_transaction(transaction)

        self.assertEqual(len(_node._transactions), 1)
        self.assertEqual(len(_node._transactions), len(_node.transactions))

        transactions_filtered_from_node = filter(
            lambda _transaction: transaction.sign == _transaction.sign, _node.transactions)

        transactions_from_node = list(
            t for t in transactions_filtered_from_node)
        self.assertEqual(list(transactions_from_node)
                         [0].sign, transaction.sign)

    def test_mine_block(self):
        _node = Node()
        sender = generate_pair_key()
        recipient = generate_pair_key()
        transaction = Transaction(sender["public_key"],
                                  recipient["public_key"], 16.58, "test")\
            .do_sign(sender["private_key"])

        _node.submit_transaction(transaction)
        _node.mine_block()


class TestApp(unittest.TestCase):
    # IMPROVE add more tests https://docs.python.org/3/library/unittest.html#basic-example
    # IMPROVE split this test into smaller tests
    # IMPROVE add node address test

    def test_transaction(self):
        sender = create_new_wallet()
        recipient = create_new_wallet()

        self.assertEqual(len(node.transactions), 2)
        self.assertEqual(len(CHAIN), 0)

        node.mine_block()

        self.assertEqual(len(node.transactions), 0)
        self.assertEqual(len(CHAIN), 2)

        trx = Transaction(sender.public_key, recipient.public_key, 17.43)\
            .do_sign(sender.private_key)
        # print(json.dumps(trx.to_dict()))

        node.submit_transaction(trx)

        self.assertEqual(len(node.transactions), 1)

        node.mine_block()

        self.assertEqual(len(node.transactions), 0)
        self.assertEqual(len(CHAIN), 3)

        self.assertIsNotNone(trx)

        for block in CHAIN.values():
            # print(json.dumps(block.to_dict()))
            if block.id == 0:
                continue

            previous_block_hash = CHAIN[block.id-1].hash
            if not validate_nonce(previous_block_hash, block.nonce):
                raise Exception("nonce invalid")
            for trx in block.data.get("transactions", []):
                jwt.decode(trx.sign, trx.sender_public_key,
                           algorithms=[ALGORITHM])

        trx2 = Transaction(sender.public_key, recipient.public_key, 17.43)\
            .do_sign(sender.private_key)
        node.submit_transaction(trx2)

        trx3 = Transaction(sender.public_key, recipient.public_key, 77.03)\
            .do_sign(sender.private_key)
        node.submit_transaction(trx3)

        sender_financial_data = sender.financial_data
        recipient_financial_data = recipient.financial_data

        self.assertEqual(
            round(sender_financial_data["balance"], 2), round(sender._balance(), 2))
        self.assertEqual(
            round(sender_financial_data["balance"], 2), round(INITIAL_BALANCE - trx.amount, 2))
        self.assertEqual(
            round(recipient_financial_data["balance"], 2), round(INITIAL_BALANCE + trx.amount, 2))

        self.assertEqual(
            round(sum(trx["amount"]
                  for trx in sender_financial_data["pending"]), 2),
            round(trx2.amount + trx3.amount, 2))

        self.assertEqual(
            round(sum(trx["amount"]
                  for trx in recipient_financial_data["pending"]), 2),
            round(trx2.amount + trx3.amount, 2))

        node.mine_block()

        self.assertEqual(
            round(sender.financial_data["balance"], 2), round(INITIAL_BALANCE - trx.amount - trx2.amount - trx3.amount, 2))
        self.assertEqual(
            round(recipient.financial_data["balance"], 2), round(INITIAL_BALANCE + trx.amount + trx2.amount + trx3.amount, 2))
