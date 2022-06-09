import json
from flask import Flask, request, jsonify, render_template, redirect, flash, session

from app.config import ALGORITHM, INITIAL_BALANCE
from app.block import CHAIN, Block, validate_nonce
from app.transaction import Transaction
from app.wallet import Wallet, create_new_wallet
from app.node import node, Node

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        create_wallet_resp = create_wallet()
        wallet = create_wallet_resp[0].get_json()

        session["user_id"] = wallet

        flash('Your wallet was successfully created and signed in!')
        flash(
            f'Will be deposit to your wallet an amount of ${INITIAL_BALANCE} on next block.')
        flash('These are your keys. The public one is your address.')
        flash('And the private one is to sign your transactions. Do not share with others.')
        flash('{public_key}'.format(**wallet).replace("\n", "\\n"))
        flash('{private_key}'.format(**wallet).replace("\n", "\\n"))
        # TODO redirect to sign in page to automatically sign in
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        wallet = Wallet(request.form["public_key"],
                        request.form["private_key"])

        session["user_id"] = wallet.to_dict()

        flash('Your wallet was successfully signed in!')
        return redirect("/")
    else:
        return render_template("signin.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/blockchain")
def blockchain():
    chain = get_chain()[0].get_json()
    return render_template("blockchain.html", blockchain=chain)


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
