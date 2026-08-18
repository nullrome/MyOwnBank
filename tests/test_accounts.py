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
        AccountNotEmptyError
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
        account_id='2',
        owner='Egor',
        balance=Decimal("4500.00")
    )

    account.freeze()

    assert account.status == AccountStatus.FROZEN


def test_checking_account_can_be_blocked():
    account = CheckingAccount(
        account_id='3',
        owner='Lera',
        balance=Decimal("1000000.00")
    )

    account.block()

    assert account.status == AccountStatus.BLOCKED


def test_frozen_checking_account_can_be_activated():
    account = CheckingAccount(
        account_id='3',
        owner='Lera',
        balance=Decimal("1000000.00")
    )

    account.freeze()
    account.activate()

    assert account.status == AccountStatus.ACTIVE