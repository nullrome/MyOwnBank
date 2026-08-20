import pytest

from decimal import Decimal

from src.domain.account_status import AccountStatus
from src.domain.checking_account import CheckingAccount
from src.domain.savings_account import SavingsAccount
from src.exceptions import (
        InvalidAmountError,
        InsufficientFundsError,
        AccountNotFoundError,
        InvalidInterestRateError,
        AccountNotEmptyError,
        InvalidAccountStatusTransitionError,
        AccountOperationNotAllowedError
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


def test_deposit_increase_checking_accounts_balance() -> None:
    account = CheckingAccount(
        account_id='1',
        owner='Roman',
        balance=Decimal("100.00")
    )

    account.deposit(Decimal("100.00"))

    assert account.balance == Decimal("200.00")


def test_withdrawal_decreases_checking_accounts_balance() -> None:
    account = CheckingAccount(
        account_id='1',
        owner='Roman',
        balance=Decimal("100.00")
    )

    account.withdraw(Decimal("50.00"))

    assert account.balance == Decimal("50.00")
    assert account.status == AccountStatus.ACTIVE


def test_several_deposits_sum_up_correctly() -> None:
    account = CheckingAccount(
        account_id='1',
        owner='Roman',
        balance=Decimal("100.00")
    )

    for _ in range(5):
        account.deposit(Decimal("50.00"))

    assert account.balance == Decimal("350.00")

    assert account.status == AccountStatus.ACTIVE


def test_frozen_account_can_deposit() -> None:
    account = CheckingAccount(
        account_id='1',
        owner='Roman',
        balance=Decimal("100.00")
    )

    account.freeze()

    account.deposit(Decimal("50.00"))

    assert account.status == AccountStatus.FROZEN and account.balance == Decimal("150.00")

    assert account.status == AccountStatus.FROZEN


def test_zero_amount_is_impossible_to_deposit() -> None:
    account = CheckingAccount(
        account_id='1',
        owner='Roman',
        balance=Decimal("100.00")
    )

    with pytest.raises(InvalidAmountError):
        account.deposit(Decimal("0.00"))

    assert account.balance == Decimal("100.00")
    assert account.status == AccountStatus.ACTIVE


def test_negative_amount_is_impossible_to_deposit() -> None:
    account = CheckingAccount(
        account_id='1',
        owner='Roman',
        balance=Decimal("100.00")
    )

    with pytest.raises(InvalidAmountError):
        account.deposit(Decimal("-5.00"))

    assert account.balance == Decimal("100.00")
    assert account.status == AccountStatus.ACTIVE


def test_infinity_amount_is_impossible_to_deposit() -> None:
    account = CheckingAccount(
        account_id='1',
        owner='Roman',
        balance=Decimal("100.00")
    )

    with pytest.raises(InvalidAmountError):
        account.deposit(Decimal("Infinity"))

    assert account.balance == Decimal("100.00")
    assert account.status == AccountStatus.ACTIVE


def test_minus_infinity_amount_is_impossible_to_deposit() -> None:
    account = CheckingAccount(
        account_id='1',
        owner='Roman',
        balance=Decimal("100.00")
    )

    with pytest.raises(InvalidAmountError):
        account.deposit(Decimal("-Infinity"))

    assert account.balance == Decimal("100.00")
    assert account.status == AccountStatus.ACTIVE


def test_nan_amount_is_impossible_to_deposit() -> None:
    account = CheckingAccount(
        account_id='1',
        owner='Roman',
        balance=Decimal("100.00")
    )

    with pytest.raises(InvalidAmountError):
        account.deposit(Decimal("NaN"))

    assert account.balance == Decimal("100.00")
    assert account.status == AccountStatus.ACTIVE


def test_int_is_impossible_to_deposit() -> None:
    account = CheckingAccount(
        account_id='1',
        owner='Roman',
        balance=Decimal("100.00")
    )

    with pytest.raises(InvalidAmountError):
        account.deposit(5)

    assert account.balance == Decimal("100.00")
    assert account.status == AccountStatus.ACTIVE


def test_float_is_impossible_to_deposit() -> None:
    account = CheckingAccount(
        account_id='1',
        owner='Roman',
        balance=Decimal("100.00")
    )

    with pytest.raises(InvalidAmountError):
        account.deposit(5.0)

    assert account.balance == Decimal("100.00")
    assert account.status == AccountStatus.ACTIVE


def test_str_is_impossible_to_deposit() -> None:
    account = CheckingAccount(
        account_id='1',
        owner='Roman',
        balance=Decimal("100.00")
    )

    with pytest.raises(InvalidAmountError):
        account.deposit("Roman")

    assert account.balance == Decimal("100.00")
    assert account.status == AccountStatus.ACTIVE


def test_none_is_impossible_to_deposit() -> None:
    account = CheckingAccount(
        account_id='1',
        owner='Roman',
        balance=Decimal("100.00")
    )

    with pytest.raises(InvalidAmountError):
        account.deposit(None)

    assert account.balance == Decimal("100.00")
    assert account.status == AccountStatus.ACTIVE


def test_blocked_account_cannot_deposit() -> None:
    account = CheckingAccount(
        account_id='1',
        owner='Roman',
        balance=Decimal("100.00")
    )

    account.block()

    with pytest.raises(AccountOperationNotAllowedError):
        account.deposit(Decimal("50.00"))

    assert account.balance == Decimal("100.00")


def test_closed_account_cannot_deposit() -> None:
    account = CheckingAccount(
        account_id='1',
        owner='Roman',
        balance=Decimal("0.00")
    )

    account.close()

    with pytest.raises(AccountOperationNotAllowedError):
        account.deposit(Decimal("100.00"))

    assert account.balance == Decimal("0.00")