from decimal import Decimal

from datetime import datetime

from src.domain.base_account import AccountStatus


class BankError(Exception):
    # base exception for all errors
    pass


class InvalidAmountError(BankError):
    # invalid amount of money for operation
    def __init__(self, amount: object):
        self.amount = amount
        super().__init__(
            f"Invalid operation amount: {self.amount!r}. "
            f"Positive finite Decimal value expected."
        )


class InsufficientFundsError(BankError):
    # not enough money on account
    def __init__(self, account_id: str, balance: Decimal, requested: Decimal):
        self.account_id = account_id
        self.balance = balance
        self.requested = requested
        super().__init__(
            f"Not enough money on account {account_id}: "
            f"balance: {self.balance}, withdrawal requested: {self.requested}."
        )


class AccountNotFoundError(BankError):
    # account was not found
    def __init__(self, account_id: str):
        self.account_id = account_id
        super().__init__(f"Account {self.account_id} is not found.")


class InvalidInterestRateError(BankError):
    # impossible interest rate
    def __init__(self, interest_rate: object):
        self.interest_rate = interest_rate
        super().__init__(
            f"Invalid interest rate: {self.interest_rate}%."
            f"Non-negative Decimal number expected."
        )


class WithdrawalLimitExceededError(BankError):
    # too many withdrawals in this month
    def __init__(self, owner: str, withdrawals_this_month: object) -> None:
        self.owner = owner
        self.withdrawals_this_month = withdrawals_this_month
        super().__init__(
            f"The user has exhausted their withdrawal limit for the month."
            f"User {self.owner} has limit per month: 3. Number of withdrawals in {datetime.now().month}: {self.withdrawals_this_month}."
        )


class InvalidTransactionError(BankError):
    # soon
    pass


class InvalidAccountStatusTransitionError(BankError):
    # invalid transition from one status to another
    def __init__(self, from_status: AccountStatus, to_status: AccountStatus) -> None:
        self.from_status = from_status
        self.to_status = to_status
        super().__init__(
            f"Invalid account status transition: {self.from_status.value} -> {self.to_status.value}."
        )