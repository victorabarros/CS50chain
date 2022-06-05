import jwt

from transaction import Transaction
from wallet import Wallet

if __name__ == "__main__":
    sender_wallet = Wallet("victor")
    recipient_wallet = Wallet("vanessa")
    print("Wallets")
    print(f"{sender_wallet.public_key}\t{sender_wallet.private_key}\t{sender_wallet.created_at}")
    print(f"{recipient_wallet.public_key}\t{recipient_wallet.private_key}\t{recipient_wallet.created_at}")

    # TODO read https://github.com/jpadilla/pyjwt/
    trx = Transaction(sender_wallet.public_key,
                      recipient_wallet.public_key, 50.2)
    print(trx.to_dict())
    encoded = trx.encode(sender_wallet.private_key)
    print(encoded)
    print(jwt.decode(encoded, sender_wallet.private_key, algorithms=trx.algorithm))
