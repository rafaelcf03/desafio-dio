from models.bank_account import BankAccount
from models.bank_client import BankClient


class BankDataBase:
    clients: list[BankClient]
    accounts: list[BankAccount]

    def __init__(self):
        self.clients: list = []
        self.accounts: list = []

    def insert_client(self, client: BankClient) -> None:
        self.clients.append(client)

    def insert_account(self, account: BankAccount) -> None:
        self.accounts.append(account)

    def verify_client_exist(self, client_ssn: str) -> BankClient | None:
        if len(self.clients) > 0:
            user_exist = [
                client for client in self.clients if client["ssn"] == client_ssn
            ]
            return user_exist[0]

    def verify_account_exist(
        self, client_ssn: str, account_n: int
    ) -> BankAccount | None:
        if len(self.accounts) > 0:
            account_exist = [
                account
                for account in self.accounts
                if account.user["ssn"] == client_ssn and account.number_id == account_n
            ]
            return account_exist[0]


storage = BankDataBase()
