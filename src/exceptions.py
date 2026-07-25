from decimal import Decimal


class BankError(Exception): # base exception for all errors
    pass


class InvalidAmountError(BankError):
    __slots__ = 'amount'

    def __init__(self, amount: object):
        self.amount = amount
        super().__init__(
            f"Invalid operation amount: {self.amount!r}. "
            f"Positive finite Decimal value expected."
        )


class InSufficientFundsError(BankError):
    __slots__ = ('account_id', 'balance', 'requested')

    def __init__(self, account_id: str, balance: Decimal, requested: Decimal):
        self.account_id = account_id
        self.balance = balance
        self.requested = requested
        super().__init__(
            f"Not enough money on account {account_id}: "
            f"balance: {self.balance}, withdrawal requested: {self.requested}."
        )


class AccountNotFoundError(BankError):
    __slots__ = 'account_id'

    def __init__(self, account_id: str):
        self.account_id = account_id
        super().__init__(f"Account {self.account_id} is not found.")


class InvalidTransactionError(BankError):
    pass