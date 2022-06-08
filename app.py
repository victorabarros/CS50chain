from flask import Flask, request, jsonify

from app.config import ALGORITHM
from app.block import CHAIN, Block, validate_nonce
from app.transaction import Transaction
from app.wallet import Wallet, create_new_wallet
from app.node import node, Node

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify({"message": "This is a Blockchain"}), 200


@app.route("/api/node")
def get_node():
    return jsonify(node.to_dict()), 200


@app.route("/api/node/mine", methods=["POST"])
def mine_block():
    return jsonify(node.mine_block().to_dict()), 200


@app.route("/api/chain")
def get_chain():
    return jsonify([block.to_dict() for block in CHAIN]), 200


@app.route("/api/wallet", methods=["POST"])
def create_wallet():
    # TODO should not expose private_key
    return jsonify(create_new_wallet().to_dict()), 201


@app.route("/api/search/wallet", methods=["POST"])
def get_wallet():
    payload = request.get_json()
    wallet = Wallet(payload["public_key"])
    return jsonify(wallet.financial_data), 200


@app.route("/api/transaction", methods=["POST"])
def submit_transaction():
    payload = request.get_json()
    trx = Transaction(payload['sender_public_key'], payload['recipient_public_key'],
                      payload['amount'], payload.get('description'))

    trx.sign = payload['sign']
    node.submit_transaction(trx)

    return jsonify(trx.to_dict()), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
