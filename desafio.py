"""
Desafio da Dio - Otimizando Sistema Bancário com Python
Objetivo geral: Separar as funções existentes de saque, depósito e extrato em funções.
"""

from dataclasses import asdict

from models.data_storage import storage
from utils.bank_utils import (
    account_balance,
    create_account,
    create_client,
    deposit,
    withdraw,
)
from utils.defines import LIMITE, LIMITE_SAQUES, MENU


def main() -> None:

    while True:
        opcao = input(MENU)

        if opcao == "c":
            name = input("Digite o nome: ")
            birth_date = input("Digite a data de nascimento (dia/mês/ano): ")
            ssn = input("Digite o CPF: ")
            address = input("Digite o endereço: ")

            try:
                client = create_client(name, birth_date, ssn, address)

                if client:
                    print(f"Cliente criado com sucesso!\n{client}")
            except Exception as e:
                print(f"\nErro ao cadastrar cliente. Erro: {e}")

        elif opcao == "b":
            ssn = input("Informe o CPF: ")

            try:
                account = create_account(ssn)
                if account:
                    print(f"Conta bancária criada com sucesso!\n{asdict(account)}")
            except Exception as e:
                print(f"\nErro ao cadastrar conta. Erro: {e}")

        elif opcao == "d":
            if len(storage.accounts) > 0:
                valor = float(input("Informe o valor do depósito: "))
                ssn = input("Informe o CPF: ")
                account_number = int(input("Informe o número da conta: "))

                try:
                    account = storage.verify_account_exist(ssn, account_number)

                    if account is None:
                        print(
                            "Não existe conta para esse CPF ou número da conta inexistente."
                        )

                    balance, statement = deposit(
                        account.balance, valor, account.statement
                    )
                    account.balance = float(balance)
                    account.statement = statement
                    print(
                        f"\nDepósito realizado com sucesso! Saldo: R${account.balance:.2f}"
                    )
                except Exception as e:
                    print(f"\nOcorreu um erro. Erro: {e}")
            else:
                print("\nNão há contas cadastradas no sistema.")

        elif opcao == "s":
            if len(storage.accounts) > 0:
                valor = float(input("Informe o valor do saque: "))
                ssn = input("Informe o CPF: ")
                account_number = int(input("Informe o número da conta: "))

                try:
                    account = storage.verify_account_exist(ssn, account_number)

                    if account is None:
                        print(
                            "\nNão existe conta para esse CPF ou número da conta inexistente."
                        )

                    balance, statement = withdraw(
                        balance=account.balance,
                        value=valor,
                        bank_statement=account.statement,
                        withdraw_count=account.withdraw_count,
                        withdraw_limit=LIMITE_SAQUES,
                        limit=LIMITE,
                    )
                    account.balance = float(balance)
                    account.statement = statement
                    account.withdraw_count += 1
                    print(
                        f"\nSaque realizado com sucesso! Saldo: R${account.balance:.2f}"
                    )
                except Exception as e:
                    print(f"\nOcorreu um erro. Erro: {e}")

            else:
                print("\nNão há contas cadastradas no sistema.")

        elif opcao == "e":
            ssn = input("Informe o CPF: ")
            account_number = int(input("Informe o número da conta: "))

            try:
                account = storage.verify_account_exist(ssn, account_number)

                if account is not None:
                    account_balance(account.balance, bank_statement=account.statement)

                else:
                    print("\nNão existe conta para esse usuário.")

            except Exception as e:
                print(f"\nOcorreu um erro. Erro: {e}")

        elif opcao == "q":
            break

        else:
            print(
                "Operação inválida, por favor selecione novamente a operação desejada."
            )


if __name__ == "__main__":
    main()
