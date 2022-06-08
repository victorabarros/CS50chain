import jwt
from datetime import datetime

from app.config import ALGORITHM


class Transaction:
    _sign = None
    # TODO add enum status (pending on node and accepted on chain)

    def __init__(self, sender_pub_key: str, recipient_pub_key: str, amount: float, description: str = None):
        self.created_at = datetime.utcnow()
        self.sender_pub_key = sender_pub_key.replace("\\n", "\n")
        self.recipient_pub_key = recipient_pub_key.replace("\\n", "\n")
        self.amount = amount
        self.description = description

    def to_dict(self, sender_private_key: str = None):
        if (sender_private_key):
            self.do_sign(sender_private_key)

        return {
            "created_at": self.created_at.isoformat(),
            "sender_pub_key": self.sender_pub_key,
            "recipient_pub_key": self.recipient_pub_key,
            "amount": self.amount,
            "description": self.description,
            "sign": self._sign,
        }

    def do_sign(self, sender_private_key: str):
        if self._sign:
            print("transaction already signed")
            return

        self._sign = jwt.encode(self.to_dict(),
                                sender_private_key, algorithm=ALGORITHM)
        jwt.decode(self._sign, self.sender_pub_key, algorithms=[ALGORITHM])
        return self

    @property
    def sign(self):
        return self._sign

    @sign.setter
    def sign(self, value):
        jwt.decode(value, self.sender_pub_key, algorithms=[ALGORITHM])
        # TODO validate decoded with self properties
        self._sign = value
