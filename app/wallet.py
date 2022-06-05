import hashlib
from datetime import datetime


class Wallet:
    def __init__(self, pub_key):
        self.created_at = datetime.utcnow()
        self.public_key = pub_key
        self.private_key = hashlib.sha256(
            f"{self.created_at}{self.public_key}".encode()).digest().hex()
