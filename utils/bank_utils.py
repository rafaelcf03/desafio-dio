from typing import TypedDict

from models.bank_account import BankAccount
from models.bank_client import BankClient
from models.data_storage import storage
from utils.defines import LIMITE
from utils.pattern_utils import clean_ssn, is_valid_ssn


class BankUtilityFunctionReturn(TypedDict):
    balance: float
    bank_statement: str


def deposit(
    balance: float, value: float, bank_statement: str, /
) -> BankUtilityFunctionReturn:
    """
    deposito: positional arguments (saldo, valor, extrato) return saldo e extrato
    """
    if value <= 0:
        raise ValueError("Operação falhou! O valor informado é inválido.")

    balance += value
    bank_statement += f"Depósito: R$ {value:.2f}\n"

    return balance, bank_statement


def withdraw(
    *,
    value: float,
    balance: float,
    bank_statement: str,
    limit: int,
    withdraw_limit: int,
    withdraw_count: int,
) -> BankUtilityFunctionReturn:
    """
    saque: argumentos keyword (saldo, valor, extrato, limite, numero_saques, limite_saques) retorno: saldo e extrato
    """
    value_overflow: bool = value > balance

    limit_overflow: bool = value > limit

    withdraw_overflow: bool = withdraw_count >= withdraw_limit

    if value_overflow:
        raise ValueError("Operação falhou! Você não tem saldo suficiente.")

    elif limit_overflow:
        raise ValueError(
            f"Operação falhou! O valor do saque excede o limite diário. Limite: R${LIMITE}"
        )

    elif withdraw_overflow:
        raise Exception("Operação falhou! Número máximo de saques excedido.")

    elif value <= 0:
        raise ValueError("Operação falhou! O valor informado é inválido.")

    balance -= value
    bank_statement += f"Saque: R$ {value:.2f}\n"
    withdraw_limit += 1

    return balance, bank_statement


def account_balance(balance: float, /, *, bank_statement: str) -> None:
    """
    extrato: argumentos keyword e positional (saldo, extrato=extrato)
    """
    print("\n================ EXTRATO ================")
    print(
        "Não foram realizadas movimentações." if not bank_statement else bank_statement
    )
    print(f"\nSaldo: R$ {balance:.2f}")
    print("==========================================")


def create_account(user_ssn: str) -> BankAccount:
    """
    criar conta corrente: armazenar em lista. conta: agencia (0001), numero da conta (sequencial iniciando em 1) e usuario.
    """
    user_exist = storage.verify_client_exist(user_ssn)

    if user_exist is None:
        raise Exception("CPF não existe no sistema.")

    account = BankAccount(user=user_exist, balance=0, statement="")
    storage.insert_account(account)

    return account


def create_client(name: str, birth_date: str, ssn: str, address: str) -> BankClient:
    """
    criar usuário: armazenar em uma lista. cliente: nome, data de nascimento, cpf e endereço[string] (logradouro, nro - bairro - cidade/sigla estado)
    obs: deve ser armazenado somente os numeros do cpf (unique)
    """

    user_exist = storage.verify_client_exist(ssn)

    if user_exist:
        raise Exception("Usuário com esse CPF já cadastrado!")

    if not is_valid_ssn(ssn):
        raise Exception(
            f"CPF com dígitos inválidos. Esperado 11 dígitos. Recebido: {len(ssn)} dígitos ({ssn})"
        )

    client = BankClient(
        name=name, birth_date=birth_date, address=address, ssn=clean_ssn(ssn)
    )
    storage.insert_client(client)

    return client
