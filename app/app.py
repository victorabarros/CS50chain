from wallet import Wallet

if __name__ == "__main__":
    wallet = Wallet("victor")
    print(
        f"Wallet\n{wallet.public_key}\t{wallet.private_key}\t{wallet.created_at}")
