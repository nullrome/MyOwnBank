import pytest

from src.exceptions import (
        InvalidAmountError,
        AccountOperationNotAllowedError
)

from src.domain.checking_account import CheckingAccount
from src.domain.account_status import AccountStatus

from decimal import Decimal


@pytest.fixture
def checking_account() -> CheckingAccount:
    return CheckingAccount(
        account_id="1",
        owner="Roman",
        balance=Decimal("100.00")
)


@pytest.mark.parametrize(
    "invalid_amount",
    [
        Decimal("0.00"),
        Decimal("-1.00"),
        Decimal("NaN"),
        Decimal("Infinity"),
        Decimal("-Infinity"),
    ],
)


def test_deposit_rejects_invalid_amount(invalid_amount, checking_account) -> None:
    with pytest.raises(InvalidAmountError):
        checking_account.deposit(invalid_amount)

    assert checking_account.balance == Decimal("100.00")


def test_deposit_increase_checking_accounts_balance(checking_account) -> None:
    checking_account.deposit(Decimal("100.00"))

    assert checking_account.balance == Decimal("200.00")


def test_several_deposits_sum_up_correctly(checking_account) -> None:
    for _ in range(5):
        checking_account.deposit(Decimal("50.00"))

    assert checking_account.balance == Decimal("350.00")
    assert checking_account.status == AccountStatus.ACTIVE


def test_frozen_account_can_deposit(checking_account) -> None:
    checking_account.freeze()

    checking_account.deposit(Decimal("50.00"))

    assert (checking_account.status == AccountStatus.FROZEN and
            checking_account.balance == Decimal("150.00"))
    assert checking_account.status == AccountStatus.FROZEN


def test_blocked_account_cannot_deposit(checking_account) -> None:
    checking_account.block()

    with pytest.raises(AccountOperationNotAllowedError):
        checking_account.deposit(Decimal("50.00"))

    assert checking_account.balance == Decimal("100.00")


def test_closed_account_cannot_deposit(checking_account) -> None:
    checking_account.close()

    with pytest.raises(AccountOperationNotAllowedError):
        checking_account.deposit(Decimal("100.00"))

    assert checking_account.balance == Decimal("0.00")