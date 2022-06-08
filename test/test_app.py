import jwt
import unittest
import json

from app.block import CHAIN, validate_nonce
from app.config import ALGORITHM, INITIAL_BALANCE
from app.transaction import Transaction
from app.node import node
from app.wallet import create_new_wallet


class TestApp(unittest.TestCase):
    # TODO add more tests https://docs.python.org/3/library/unittest.html#basic-example

    def test_transaction(self):
        sender = create_new_wallet()
        recipient = create_new_wallet()

        self.assertEqual(len(node.transactions), 2)
        self.assertEqual(len(CHAIN), 1)

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

        for block in CHAIN:
            # print(json.dumps(block.to_dict()))
            if block.id == 0:
                continue

            previous_block_hash = CHAIN[block.id-1].hash
            if not validate_nonce(previous_block_hash, block.nonce):
                raise Exception("nonce invalid")
            for trx in block.data.get("transactions", []):
                jwt.decode(trx.sign, trx.sender_pub_key,
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
            round(sender_financial_data["balance"], 2),
            round(INITIAL_BALANCE - trx.amount, 2))
        self.assertEqual(
            round(recipient_financial_data["balance"], 2),
            round(INITIAL_BALANCE + trx.amount, 2))

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
            round(sender.financial_data["balance"], 2),
            round(INITIAL_BALANCE - trx.amount - trx2.amount - trx3.amount, 2))
        self.assertEqual(
            round(recipient.financial_data["balance"], 2),
            round(INITIAL_BALANCE + trx.amount + trx2.amount + trx3.amount, 2))
