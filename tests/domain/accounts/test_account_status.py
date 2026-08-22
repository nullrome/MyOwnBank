import pytest

from decimal import Decimal

from src.domain.account_status import AccountStatus
from src.domain.checking_account import CheckingAccount
from src.exceptions import (
        AccountNotEmptyError,
        InvalidAccountStatusTransitionError
)


def test_new_checking_account_is_active() -> None:
    account = CheckingAccount(
        account_id='1',
        owner='Roman',
        balance=Decimal("100.00")
    )

    assert account.status == AccountStatus.ACTIVE


def test_active_checking_account_can_be_frozen() -> None:
    account = CheckingAccount(
        account_id='1',
        owner='Roman',
        balance=Decimal("100.00")
    )

    account.freeze()

    assert account.status == AccountStatus.FROZEN


def test_active_checking_account_can_be_blocked() -> None:
    account = CheckingAccount(
        account_id='1',
        owner='Roman',
        balance=Decimal("100.00")
    )

    account.block()

    assert account.status == AccountStatus.BLOCKED


def test_frozen_checking_account_can_be_activated() -> None:
    account = CheckingAccount(
        account_id='1',
        owner='Roman',
        balance=Decimal("100.00")
    )

    account.freeze()
    account.activate()

    assert account.status == AccountStatus.ACTIVE


def test_closed_checking_account_cannot_be_activated() -> None:
    account = CheckingAccount(
        account_id='1',
        owner='Roman',
        balance=Decimal("0.00")
    )

    account.close()

    with pytest.raises(InvalidAccountStatusTransitionError):
        account.activate()


def test_not_empty_checking_account_cannot_be_closed() -> None:
    account = CheckingAccount(
        account_id='1',
        owner='Roman',
        balance=Decimal("100.00")
    )

    with pytest.raises(AccountNotEmptyError):
        account.close()


def test_active_checking_account_cannot_be_activated() -> None:
    account = CheckingAccount(
        account_id='1',
        owner='Roman',
        balance=Decimal("100.00")
    )

    with pytest.raises(InvalidAccountStatusTransitionError):
        account.activate()


def test_frozen_checking_account_cannot_be_frozen() -> None:
    account = CheckingAccount(
        account_id='1',
        owner='Roman',
        balance=Decimal("100.00")
    )

    account.freeze()

    with pytest.raises(InvalidAccountStatusTransitionError):
        account.freeze()


def test_frozen_checking_account_can_be_blocked() -> None:
    account = CheckingAccount(
        account_id='1',
        owner='Roman',
        balance=Decimal("100.00")
    )

    account.freeze()
    account.block()

    assert account.status == AccountStatus.BLOCKED


def test_blocked_checking_account_cannot_be_activated() -> None:
    account = CheckingAccount(
        account_id='1',
        owner='Roman',
        balance=Decimal("100.00")
    )

    account.block()

    with pytest.raises(InvalidAccountStatusTransitionError):
        account.activate()


def test_blocked_checking_account_cannot_be_frozen() -> None:
    account = CheckingAccount(
        account_id='1',
        owner='Roman',
        balance=Decimal("100.00")
    )

    account.block()

    with pytest.raises(InvalidAccountStatusTransitionError):
        account.freeze()


def test_blocked_checking_account_cannot_be_blocked() -> None:
    account = CheckingAccount(
        account_id='1',
        owner='Roman',
        balance=Decimal("100.00")
    )

    account.block()

    with pytest.raises(InvalidAccountStatusTransitionError):
        account.block()
