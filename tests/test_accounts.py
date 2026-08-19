import pytest

from decimal import Decimal

from src.domain.account_status import AccountStatus
from src.domain.base_account import BaseAccount
from src.domain.checking_account import CheckingAccount
from src.domain.savings_account import SavingsAccount
from src.exceptions import (
        InvalidAmountError,
        InsufficientFundsError,
        AccountNotFoundError,
        InvalidInterestRateError,
        AccountNotEmptyError,
        InvalidAccountStatusTransitionError
)


def test_new_checking_account_is_active():
    account = CheckingAccount(
        account_id='1',
        owner='Roman',
        balance=Decimal("100.00")
    )

    assert account.status == AccountStatus.ACTIVE


def test_checking_account_can_be_frozen():
    account = CheckingAccount(
        account_id='1',
        owner='Roman',
        balance=Decimal("100.00")
    )

    account.freeze()

    assert account.status == AccountStatus.FROZEN


def test_checking_account_can_be_blocked():
    account = CheckingAccount(
        account_id='1',
        owner='Roman',
        balance=Decimal("100.00")
    )

    account.block()

    assert account.status == AccountStatus.BLOCKED


def test_frozen_checking_account_can_be_activated():
    account = CheckingAccount(
        account_id='1',
        owner='Roman',
        balance=Decimal("100.00")
    )

    account.freeze()
    account.activate()

    assert account.status == AccountStatus.ACTIVE


def test_closed_checking_account_cannot_be_activated():
    account = CheckingAccount(
        account_id='1',
        owner='Roman',
        balance=Decimal("0.00")
    )

    account.close()

    with pytest.raises(InvalidAccountStatusTransitionError):
        account.activate()


def test_not_empty_checking_account_cannot_be_closed():
    account = CheckingAccount(
        account_id='1',
        owner='Roman',
        balance=Decimal("100.00")
    )

    with pytest.raises(AccountNotEmptyError):
        account.close()


def test_deposit_increase_checkings_account_balance():
    account = CheckingAccount(
        account_id='1',
        owner='Roman',
        balance=Decimal("100.00")
    )

    account.deposit(Decimal("100.00"))

    assert account.balance == Decimal("200.00")


def test_withdrawal_decreases_checkings_account_balance():
    account = CheckingAccount(
        account_id='1',
        owner='Roman',
        balance=Decimal("100.00")
    )

    account.withdraw(Decimal("50.00"))

    assert account.balance == Decimal("50.00")