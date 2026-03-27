import itertools
from dataclasses import dataclass, field

from models.bank_client import BankClient


@dataclass(slots=True)
class BankAccount:
    user: BankClient
    balance: float = 0.0
    statement: str = ""
    withdraw_count: int = 0
    agency: str = field(init=False, default="0001", repr=True)
    number_id: int = field(init=False, repr=True)

    _id_counter = 1

    def __post_init__(self):
        self.number_id = BankAccount._id_counter
        BankAccount._id_counter += 1
