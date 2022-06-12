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
        self.assertEqual(len(_node._nodes), len(_node.nodes))

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

        self.assertEqual(len(_node.transactions), 1)

        transactions_filtered_from_node = filter(
            lambda _transaction: transaction.sign == _transaction.sign, _node.transactions)

        transactions_from_node = list(
            t for t in transactions_filtered_from_node)
        self.assertEqual(list(transactions_from_node)
                         [0].sign, transaction.sign)

    def test_add_address(self):
        _node = Node()
        _second_node_address = "http://foo.bar"
        _node.add_node_address(_second_node_address)
        self.assertEqual(len(_node.nodes), 1)
        nodes = list(n for n in _node.nodes)
        self.assertEqual(nodes[0], _second_node_address)

        # can't add the same
        _node.add_node_address(_second_node_address)
        self.assertEqual(len(_node.nodes), 1)
        # self.assertEqual(len(Node().nodes), 0)  # TODO WHY IS FAILING?????

    def test_mine_block(self):
        _node = Node()
        _node.mine_block()  # to clear block

        sender = generate_pair_key()
        recipient = generate_pair_key()
        transaction = Transaction(sender["public_key"],
                                  recipient["public_key"], 16.58, "test")\
            .do_sign(sender["private_key"])

        _node.submit_transaction(transaction)
        new_block = _node.mine_block()
        last_block = CHAIN[len(CHAIN)-1]
        self.assertEqual(id(last_block), id(new_block))

        block_transactions = last_block.data.get("transactions", [])

        self.assertEqual(len(block_transactions), 1)

        transaction_from_chain = block_transactions[0]
        self.assertEqual(id(transaction_from_chain), id(transaction))

    def test_clear_transactions(self):
        _node = Node()
        _node.clear_transactions()
        self.assertEqual(len(_node.transactions), 0)

        sender = generate_pair_key()
        recipient = generate_pair_key()
        transaction = Transaction(sender["public_key"],
                                  recipient["public_key"], 16.58, "test")\
            .do_sign(sender["private_key"])

        _node.submit_transaction(transaction)
        self.assertEqual(len(_node.transactions), 1)
        _node.clear_transactions()
        self.assertEqual(len(_node.transactions), 0)

    def test_to_dict(self):
        _node = Node()
        _node.clear_transactions()
        self.assertEqual(len(_node.transactions), 0)

        sender = generate_pair_key()
        recipient = generate_pair_key()

        _node.submit_transaction(
            Transaction(sender["public_key"],
                        recipient["public_key"], 16.58, "test")
            .do_sign(sender["private_key"]))

        _node.add_node_address("http://bar.foo")

        _node_dict = _node.to_dict()

        for idx, address in enumerate(_node.nodes):
            self.assertEqual(address, _node_dict["nodes"][idx])

        for idx, trasaction in enumerate(_node.transactions):
            self.assertEqual(
                trasaction.sign, _node_dict["transactions"][idx]["sign"])
            self.assertEqual(trasaction.sender_public_key,
                             _node_dict["transactions"][idx]["sender_public_key"])
            self.assertEqual(trasaction.recipient_public_key,
                             _node_dict["transactions"][idx]["recipient_public_key"])
            self.assertEqual(trasaction.amount,
                             _node_dict["transactions"][idx]["amount"])
            self.assertEqual(trasaction.description,
                             _node_dict["transactions"][idx]["description"])


class TestApp(unittest.TestCase):
    def test_all(self):
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
