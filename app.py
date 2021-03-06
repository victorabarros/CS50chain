from flask import Flask, request, jsonify, render_template, redirect, flash, session

from app.config import INITIAL_BALANCE, PORT
from app.block import CHAIN, Blockchain
from app.transaction import Transaction
from app.wallet import Wallet
from app.node import NODE

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
def handle_index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def handle_register():
    if request.method == "POST":
        wallet = Wallet.new()

        print(wallet.to_dict())
        session["user_id"] = wallet.to_dict()

        flash('Your wallet was successfully created and signed in!')
        flash(
            f'Will be deposit to your wallet an amount of ${INITIAL_BALANCE} on next block.')
        flash('These are your keys. The public one is your address.')
        flash('And the private one is to sign your transactions. Do not share with others.')
        flash(wallet.public_key.replace("\n", "\\n"))
        flash(wallet.private_key.replace("\n", "\\n"))
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/signin", methods=["GET", "POST"])
def handle_signin():
    if request.method == "POST":
        wallet = Wallet(request.form["public_key"],
                        request.form["private_key"])
        print(wallet.to_dict())
        session["user_id"] = wallet.to_dict()

        flash('Your wallet was successfully signed in!')
        return redirect("/")
    else:
        return render_template("signin.html")


@app.route("/logout")
def handle_logout():
    session.clear()
    return redirect("/")


@app.route("/blockchain")
def handle_blockchain():
    chain = api_get_chain()[0].get_json()
    return render_template("blockchain.html", blockchain=chain)


@app.route("/node", methods=["GET", "POST"])
def handle_node():
    if request.method == "POST":
        api_add_node_address()
    node = api_get_node()[0].get_json()
    return render_template("node.html", transactions=node["transactions"], nodes=node["nodes"])


@app.route("/node/mine", methods=["POST"])
def handle_mine_node():
    api_mine_block()
    flash('Node was successfully mined!')
    flash('See on Blockchain tab')
    return redirect("/node")


@app.route("/wallet")
def handle_wallet():
    wallet = Wallet(session["user_id"]["public_key"])

    return render_template("wallet.html",
                           public_key=wallet.public_key.replace("\n", "\\n"),
                           **wallet.financial_data)


@app.route("/transaction", methods=["GET", "POST"])
def handle_transaction():
    transaction = None
    if request.method == "POST":
        recipient_public_key = request.form["recipient_public_key"]
        recipient_public_key = "{}{}{}".format(
            recipient_public_key[:26],
            recipient_public_key[26:-24].replace(" ", "\n"),
            recipient_public_key[-24:]
        )
        amount = int(request.form["amount"])
        description = request.form["description"] or None

        trx = Transaction(session["user_id"]["public_key"],
                          recipient_public_key,
                          amount,
                          description)

        NODE.submit_transaction(trx.do_sign(
            session["user_id"]["private_key"]))

        transaction = trx.to_dict()

        flash('Transaction was successfully submitted!')
        flash('See on Node tab')

    return render_template("transaction.html", transaction=transaction)


@app.route("/api/node")
def api_get_node():
    return jsonify(NODE.to_dict()), 200


@app.route("/api/node/address", methods=["POST"])
def api_add_node_address():
    address = request.form.get("address") or request.get_json().get("address")
    NODE.add_node_address(address)
    return jsonify(), 201


@app.route("/api/node/transactions", methods=["DELETE"])
def api_clear_node_transactions():
    NODE.clear_transactions()
    return jsonify(), 200


@app.route("/api/node/mine", methods=["POST"])
def api_mine_block():
    return jsonify(NODE.mine_block().to_dict()), 200


@app.route("/api/chain")
def api_get_chain():
    return jsonify(list(block.to_dict() for block in CHAIN.values())), 200


@app.route("/api/chain", methods=["POST"])
def sync_chain():
    NODE.sync_blockchain()
    return jsonify(), 200


@app.route("/api/wallet", methods=["POST"])
def api_create_wallet():
    return jsonify(Wallet.new().to_dict()), 201


@app.route("/api/search/wallet", methods=["POST"])
def api_search_wallet():
    payload = request.get_json()
    wallet = Wallet(payload["public_key"])
    return jsonify(wallet.financial_data), 200


@app.route("/api/transaction", methods=["POST"])
def api_submit_transaction():
    payload = request.get_json()
    trx = Transaction(payload['sender_public_key'].replace("\\n", "\n"),
                      payload['recipient_public_key'].replace("\\n", "\n"),
                      payload['amount'], payload.get('description'))

    trx.sign = payload['sign']
    NODE.submit_transaction(trx)

    return jsonify(trx.to_dict()), 201


if __name__ == "__main__":
    Blockchain.load_chain()
    NODE.sync()
    app.run(host="0.0.0.0", port=PORT, debug=True)
