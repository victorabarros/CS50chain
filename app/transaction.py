import jwt
from datetime import datetime


class Transaction:
    algorithm = "HS256"
    sign = None

    def __init__(self, sender_pub_key: str, recipient_pub_key: str, amount: float, description: str = None):
        self.created_at = datetime.utcnow()
        self.sender_pub_key = sender_pub_key
        self.recipient_pub_key = recipient_pub_key
        self.amount = amount
        self.description = description

    def to_dict(self):
        return {
            "created_at": str(self.created_at),
            "sender_pub_key": self.sender_pub_key,
            "recipient_pub_key": self.recipient_pub_key,
            "amount": self.amount,
            "description": self.description,
            "sign": self.sign,
        }

    def encode(self, sender_private_key: str):
        # TODO try RSA256 https://pyjwt.readthedocs.io/en/stable/usage.html#encoding-decoding-tokens-with-rs256-rsa
        return jwt.encode(self.to_dict(),
                          sender_private_key, algorithm=self.algorithm)
