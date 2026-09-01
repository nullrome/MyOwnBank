import pytest

from decimal import Decimal

from domain.accounts.savings_account import SavingsAccount

from src.exceptions import (InvalidInterestRateError,
                            WithdrawalLimitExceededError,
                            InsufficientFundsError,
                            InvalidAmountError,
                            AccountOperationNotAllowedError,
                            AccountNotEmptyError)

from src.domain.account_status import AccountStatus


@pytest.fixture
def savings_account() -> SavingsAccount:
    savings_account = SavingsAccount(account_id="1",
                                     owner="Roman",
                                     interest_rate=Decimal("10.00"),
                                     balance=Decimal("100.00")
                                     )
    return savings_account


@pytest.mark.parametrize(
    "invalid_interest_rate",
    [
        Decimal("0.00"),
        Decimal("Infinity"),
        Decimal("-Infinity"),
        Decimal("Nan"),
        5,
        10.5,
        "Roman",
        None
    ]
)


def test_attempt_to_set_invalid_interest_rate(invalid_interest_rate, savings_account) -> None:
    with pytest.raises(InvalidInterestRateError):
        savings_account.interest_rate = invalid_interest_rate

    assert savings_account.balance == Decimal("100.00")
    assert savings_account.interest_rate == Decimal("10.00")
    assert savings_account.status == AccountStatus.ACTIVE


def test_attempt_to_set_valid_interest_rate(savings_account) -> None:
    savings_account.interest_rate = Decimal("5.00")

    assert savings_account.interest_rate == Decimal("5.00")
    assert savings_account.status == AccountStatus.ACTIVE


def test_withdrawals_limit_works_correctly(savings_account) -> None:
    assert savings_account.withdrawals_this_month == 0

    savings_account.withdraw(Decimal("10.00"))

    assert savings_account.withdrawals_this_month == 1

    savings_account.withdraw(Decimal("10.00"))

    assert savings_account.withdrawals_this_month == 2

    savings_account.withdraw(Decimal("10.00"))

    assert savings_account.withdrawals_this_month == 3

    with pytest.raises(WithdrawalLimitExceededError):
        savings_account.withdraw(Decimal("10.00"))

    assert savings_account.withdrawals_this_month == 3
    assert savings_account.balance == Decimal("70.00")


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


def test_attempt_to_withdraw_invalid_amount(savings_account, invalid_amount) -> None:
    with pytest.raises(InvalidAmountError):
        savings_account.withdraw(invalid_amount)

    assert savings_account.withdrawals_this_month == 0
    assert savings_account.balance == Decimal("100.00")


def test_attempt_to_withdraw_the_whole_balance(savings_account) -> None:
    savings_account.withdraw(Decimal("100.00"))

    assert savings_account.balance == Decimal("0.00")
    assert savings_account.withdrawals_this_month == 1


def test_attempt_to_withdraw_more_than_possible(savings_account) -> None:
    with pytest.raises(InsufficientFundsError):
        savings_account.withdraw(Decimal("150.00"))

    assert savings_account.withdrawals_this_month == 0
    assert savings_account.balance == Decimal("100.00")


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


def test_attempt_to_deposit_invalid_amount(savings_account, invalid_amount) -> None:
    with pytest.raises(InvalidAmountError):
        savings_account.deposit(invalid_amount)

    assert savings_account.withdrawals_this_month == 0
    assert savings_account.balance == Decimal("100.00")


def test_attempt_to_deposit_valid_amount(savings_account) -> None:
    savings_account.deposit(Decimal("100.00"))

    assert savings_account.balance == Decimal("200.00")


def test_blocked_account_cannot_operate_with_money(savings_account) -> None:
    savings_account.block()

    with pytest.raises(AccountOperationNotAllowedError):
        savings_account.deposit(Decimal("100.00"))

    with pytest.raises(AccountOperationNotAllowedError):
        savings_account.withdraw(Decimal("50.00"))

    assert savings_account.balance == Decimal("100.00")
    assert savings_account.status == AccountStatus.BLOCKED
    assert savings_account.withdrawals_this_month == 0


def test_account_cannot_be_closed_with_non_zero_balance(savings_account) -> None:
    with pytest.raises(AccountNotEmptyError):
        savings_account.close()

    assert savings_account.status == AccountStatus.ACTIVE


def test_attempt_to_close_empty_account(savings_account) -> None:
    savings_account.withdraw(Decimal("100.00"))
    savings_account.close()

    assert savings_account.status == AccountStatus.CLOSED


def test_closed_account_cannot_operate_with_money(savings_account) -> None:
    savings_account.withdraw(Decimal("100.00"))
    savings_account.close()

    with pytest.raises(AccountOperationNotAllowedError):
        savings_account.deposit(Decimal("100.00"))

    with pytest.raises(AccountOperationNotAllowedError):
        savings_account.withdraw(Decimal("50.00"))

    assert savings_account.balance == Decimal("0.00")
    assert savings_account.status == AccountStatus.CLOSED
    assert savings_account.withdrawals_this_month == 1
