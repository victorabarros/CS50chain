import unittest
from app.transaction import Transaction

from app.wallet import create_new_wallet


class TestApp(unittest.TestCase):
    # TODO add more tests https://docs.python.org/3/library/unittest.html#basic-example

    def test_transaction(self):
        sender = create_new_wallet()
        recipient = create_new_wallet()
        trx = Transaction(sender.public_key, recipient.public_key, 10.3)\
            .do_sign(sender.private_key)
        self.assertIsNotNone(trx)
        print(trx.to_dict())
