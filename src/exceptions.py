from decimal import Decimal

from datetime import datetime

from src.domain.account_status import AccountStatus


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
    def __init__(self, account_id: str) -> None:
        self.account_id = account_id
        super().__init__(
            f"Account {self.account_id} is not found."
        )


class InvalidInterestRateError(BankError):
    # impossible interest rate
    def __init__(self, interest_rate: object) -> None:
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


class InvalidAccountStatusTransitionError(BankError):
    # invalid transition from one status to another
    def __init__(self, from_status: AccountStatus, to_status: AccountStatus) -> None:
        self.from_status = from_status
        self.to_status = to_status
        super().__init__(
            f"Invalid account status transition: {self.from_status.value} -> {self.to_status.value}."
        )


class AccountNotEmptyError(BankError):
    # impossibility of account closing
    def __init__(self, balance: Decimal) -> None:
        self.balance = balance
        super().__init__(
            f"Cannot close account with balance with non-zero balance: {self.balance:.2f}."
        )


class AccountOperationNotAllowedError(BankError):
    # now operation is not allowed
    def __init__(self, operation: str, status: AccountStatus) -> None:
        self.operation = operation
        self.status = status
        super().__init__(
            f'Operation "{self.operation}" is not allowed for account in "{self.status}" status.'
        )


class InvalidCreditLimitError(BankError):
    # invalid credit limit
    def __init__(self, credit_limit: Decimal) -> None:
        self.credit_limit = credit_limit
        super().__init__(
            f'Invalid credit limit: {self.credit_limit!r}.'
            f'Positive finite Decimal value expected.'
        )


class OutstandingDebtError(BankError):
    # user must pay in addition
    def __init__(self, debt: Decimal) -> None:
        self.debt = debt
        super().__init__(
            f"Cannot close credit account with outstanding debt: {self.debt}."
        )


class CreditLimitExceededError(BankError):
    # user wanna spend more than possible
    def __init__(self, amount: Decimal, available_credit: Decimal) -> None:
        self.amount = amount
        self.available_credit = available_credit
        super().__init__(
            f"Credit limit exceeded: requested {self.amount}, "
            f"available credit is {self.available_credit}."
        )


class RepaymentExceedsDebtError(BankError):
    # repayment is bigger than user's debt
    def __init__(self, amount: Decimal, debt: Decimal) -> None:
        self.amount = amount
        self.debt = debt
        super().__init__(
            f"Repayment amount {self.amount} exceeds outstanding debt {self.debt}."
        )


class InvalidInterestPeriodError(BankError):
    # invalid days of credit
    def __init__(self, days: int) -> None:
        self.days = days
        super().__init__(
            f"Invalid interest period: {self.days}."
            f"Non-negative finite integer expected."
        )


class InvalidDebtError(BankError):
    # invalid debt
    def __init__(self, debt: Decimal) -> None:
        self.debt = debt
        super().__init__(
            f"Invalid debt: {self.debt}."
            f"Non-negative finite decimal expected."
        )