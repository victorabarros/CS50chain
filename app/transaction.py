import jwt
from datetime import datetime

from app.config import ALGORITHM


class Transaction:
    # IMPROVE add enum status (pending on node and accepted on chain)
    _sender_public_key = None
    _recipient_public_key = None
    _amount = None
    _description = None
    _sign = None
    _created_at = None

    def __init__(self, sender_public_key: str, recipient_public_key: str, amount: float, description: str = None, **kwargs):
        self._created_at = datetime.utcnow()
        self._sender_public_key = sender_public_key.replace("\\n", "\n")
        self._recipient_public_key = recipient_public_key.replace("\\n", "\n")
        self._amount = amount
        self._description = description

    def to_dict(self, sender_private_key: str = None):
        if (sender_private_key):
            self.do_sign(sender_private_key)

        return {
            "created_at": self.created_at.isoformat(),
            "sender_public_key": self.sender_public_key,
            "recipient_public_key": self.recipient_public_key,
            "amount": self.amount,
            "description": self.description,
            "sign": self._sign,
        }

    @staticmethod
    def from_dict(**kwargs):
        t = Transaction(**kwargs)
        t._created_at = datetime.fromisoformat(kwargs["created_at"])
        t.sign = kwargs["sign"]
        return t

    def do_sign(self, sender_private_key: str):
        if self._sign:
            print("transaction already signed")
            return

        self._sign = jwt.encode(self.to_dict(),
                                sender_private_key, algorithm=ALGORITHM)
        jwt.decode(self._sign, self.sender_public_key, algorithms=[ALGORITHM])
        return self

    @property
    def sign(self):
        return self._sign

    @sign.setter
    def sign(self, value):
        jwt.decode(value, self.sender_public_key, algorithms=[ALGORITHM])
        self._sign = value

    @property
    def created_at(self):
        return self._created_at

    @property
    def sender_public_key(self):
        return self._sender_public_key

    @property
    def recipient_public_key(self):
        return self._recipient_public_key

    @property
    def amount(self):
        return self._amount

    @property
    def description(self):
        return self._description
