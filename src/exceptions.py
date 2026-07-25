from decimal import Decimal

from datetime import datetime


class BankError(Exception): # base exception for all errors
    pass


class InvalidAmountError(BankError):
    def __init__(self, amount: object):
        self.amount = amount
        super().__init__(
            f"Invalid operation amount: {self.amount!r}. "
            f"Positive finite Decimal value expected."
        )


class InsufficientFundsError(BankError):
    def __init__(self, account_id: str, balance: Decimal, requested: Decimal):
        self.account_id = account_id
        self.balance = balance
        self.requested = requested
        super().__init__(
            f"Not enough money on account {account_id}: "
            f"balance: {self.balance}, withdrawal requested: {self.requested}."
        )


class AccountNotFoundError(BankError):
    def __init__(self, account_id: str):
        self.account_id = account_id
        super().__init__(f"Account {self.account_id} is not found.")


class InvalidInterestRateError(BankError):
    def __init__(self, interest_rate: object):
        self.interest_rate = interest_rate
        super().__init__(
            f"Invalid interest rate: {self.interest_rate}%."
            f"Non-negative Decimal number expected."
        )


class WithdrawalLimitExceededError(BankError):
    def __init__(self, account_id: str, owner: str, balance: Decimal, withdrawals_this_month: object, interest_rate: Decimal) -> None:
        self.account_id = account_id
        self.owner = owner
        self.balance = balance
        self.withdrawals_this_month = withdrawals_this_month
        self.interest_rate = interest_rate
        super().__init__(
            f"The user has exhausted their withdrawal limit for the month."
            f"User {self.owner} has limit per month: 3. Number of withdrawals in {datetime.datetime.now().month}: {self.withdrawals_this_month}."
        )


class InvalidTransactionError(BankError):
    pass