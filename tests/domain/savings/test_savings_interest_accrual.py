from collections.abc import Callable

import pytest

from uuid import UUID
from decimal import Decimal
from datetime import date

from src.exceptions import InvalidAmountError

from src.domain.savings.interest_accrual import SavingsInterestAccrual


ACCRUAL_ID = UUID("12345678-1234-5678-1234-567812345678")


VALID_ACCRUAL_DATA = {
    "account_id": "savings-accrual-1",
    "accrual_id": ACCRUAL_ID,
    "accrual_date": date(2026, 12, 10),
    "amount": Decimal("100.00"),
}


@pytest.fixture
def interest_accrual() -> SavingsInterestAccrual:
    return SavingsInterestAccrual(**VALID_ACCRUAL_DATA)


def test_entity_saves_all_values(interest_accrual: SavingsInterestAccrual) -> None:
    assert interest_accrual.account_id == "savings-accrual-1"
    assert interest_accrual.accrual_id == ACCRUAL_ID
    assert interest_accrual.accrual_date == date(2026, 12, 10)
    assert interest_accrual.amount == Decimal("100.00")


@pytest.mark.parametrize(
    "amount",
    [
        Decimal("0.00"),
        Decimal("-1.00"),
        Decimal("NaN"),
        Decimal("Infinity"),
        Decimal("-Infinity"),
        100,
        100.0,
        "100.00",
        None,
    ],
)
def test_invalid_amount_is_rejected(amount: object) -> None:
    data = VALID_ACCRUAL_DATA | {"amount": amount}

    with pytest.raises(InvalidAmountError):
        SavingsInterestAccrual(**data)