import pytest

from decimal import Decimal

from src.exceptions import InvalidAmountError, InsufficientFundsError, AccountOperationNotAllowedError

from src.domain.checking_account import CheckingAccount
from src.domain.account_status import AccountStatus

@pytest.fixture
def checking_account() -> CheckingAccount:
    return CheckingAccount(
        account_id="1",
        owner="Roman",
        balance=Decimal("100.00")
    )


def test_withdrawal_amount_is_less_than_balance(checking_account) -> None:
    checking_account.withdraw(Decimal("50.00"))

    assert checking_account.balance == Decimal("50.00")
    assert checking_account.status == AccountStatus.ACTIVE


def test_withdrawal_amount_is_equal_to_the_balance(checking_account) -> None:
    checking_account.withdraw(Decimal("100.00"))

    assert checking_account.balance == Decimal("0.00")
    assert checking_account.status == AccountStatus.ACTIVE


def test_consequent_several_withdrawals(checking_account) -> None:
    for _ in range(5):
        checking_account.withdraw(Decimal("10.00"))

    assert checking_account.balance == Decimal("50.00")
    assert checking_account.status == AccountStatus.ACTIVE


def test_frozen_account_can_withdraw(checking_account) -> None:
    checking_account.freeze()
    checking_account.withdraw(Decimal("50.00"))

    assert checking_account.balance == Decimal("50.00")
    assert checking_account.status == AccountStatus.FROZEN


def test_withdrawal_amount_is_bigger_than_balance(checking_account) -> None:
    with pytest.raises(InsufficientFundsError):
        checking_account.withdraw(Decimal("150.00"))

    assert checking_account.balance == Decimal("100.00")
    assert checking_account.status == AccountStatus.ACTIVE


def test_attempt_to_withdraw_positive_amount_while_zero_balance() -> None:
    checking_account = CheckingAccount(
        account_id="1",
        owner="Roman",
        balance=Decimal("0.00")
    )

    with pytest.raises(InsufficientFundsError):
        checking_account.withdraw(Decimal("100.00"))

    assert checking_account.balance == Decimal("0.00")
    assert checking_account.status == AccountStatus.ACTIVE


@pytest.mark.parametrize(
    "invalid_amount",
    [
        Decimal("0.00"),
        Decimal("-1.00"),
        Decimal("Infinity"),
        Decimal("-Infinity"),
        Decimal("NaN"),
        10,
        10.0,
        "Roman",
        None
    ],
)


def test_attempt_to_withdraw_invalid_amount(checking_account, invalid_amount) -> None:
    with pytest.raises(InvalidAmountError):
        checking_account.withdraw(invalid_amount)

    assert checking_account.balance == Decimal("100.00")
    assert checking_account.status == AccountStatus.ACTIVE


def test_blocked_account_cannot_withdraw(checking_account) -> None:
    checking_account.block()

    with pytest.raises(AccountOperationNotAllowedError):
        checking_account.withdraw(Decimal("50.00"))

    assert checking_account.balance == Decimal("100.00")
    assert checking_account.status == AccountStatus.BLOCKED


def test_closed_account_cannot_withdraw() -> None:
    checking_account = CheckingAccount(
        account_id="1",
        owner="Roman",
        balance=Decimal("0.00")
    )

    checking_account.close()

    with pytest.raises(AccountOperationNotAllowedError):
        checking_account.withdraw(Decimal("100.00"))

    assert checking_account.balance == Decimal("0.00")
    assert checking_account.status == AccountStatus.CLOSED
