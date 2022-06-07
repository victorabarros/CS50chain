from flask import Flask, jsonify

from app.config import ALGORITHM
from app.block import CHAIN, Block, validate_nonce
from app.transaction import Transaction
from app.wallet import Wallet
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


if __name__ == "__main__":
    app.run(debug=True)
