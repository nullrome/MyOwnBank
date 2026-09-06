import pytest

from datetime import date
from decimal import Decimal
from typing import Any

from src.domain.credit.interest_accrual import InterestAccrual
from src.exceptions import (
    InvalidInterestAccrualError,
    InvalidInterestAccrualPeriodError,
)

from uuid import UUID


ACCRUAL_ID = UUID("12345678-1234-5678-1234-567812345678")


VALID_ACCRUAL_DATA = {
    "accrual_id":ACCRUAL_ID,
    "account_id": "credit-1",
    "period_start": date(2026, 8, 1),
    "period_end": date(2026, 9, 1),
    "debt_before": Decimal("10000.00"),
    "annual_rate": Decimal("15.00"),
    "amount": Decimal("127.40"),
}


class TestInterestAccrualCreation:
    def test_interest_accrual_stores_all_values(self) -> None:
        accrual = InterestAccrual(**VALID_ACCRUAL_DATA)

        assert accrual.accrual_id == ACCRUAL_ID
        assert accrual.account_id == "credit-1"
        assert accrual.period_start == date(2026, 8, 1)
        assert accrual.period_end == date(2026, 9, 1)
        assert accrual.debt_before == Decimal("10000.00")
        assert accrual.annual_rate == Decimal("15.00")
        assert accrual.amount == Decimal("127.40")


class TestInterestAccrualIdentifiersValidation:
    @pytest.mark.parametrize(
        "accrual_id",
        [
            "",
            123,
            None,
            Decimal("1"),
        ],
    )
    def test_invalid_accrual_id_is_forbidden(
        self,
        accrual_id: Any,
    ) -> None:
        data = VALID_ACCRUAL_DATA | {
            "accrual_id": accrual_id,
        }

        with pytest.raises(InvalidInterestAccrualError):
            InterestAccrual(**data)


    @pytest.mark.parametrize(
        "account_id",
        [
            "",
            123,
            None,
            Decimal("1"),
        ],
    )
    def test_invalid_account_id_is_forbidden(
        self,
        account_id: Any,
    ) -> None:
        data = VALID_ACCRUAL_DATA | {
            "account_id": account_id,
        }

        with pytest.raises(InvalidInterestAccrualError):
            InterestAccrual(**data)


class TestInterestAccrualPeriodValidation:
    def test_period_end_equal_to_period_start_is_forbidden(self) -> None:
        data = VALID_ACCRUAL_DATA | {
            "period_start": date(2026, 9, 1),
            "period_end": date(2026, 9, 1),
        }

        with pytest.raises(InvalidInterestAccrualPeriodError):
            InterestAccrual(**data)


    def test_period_end_before_period_start_is_forbidden(self) -> None:
        data = VALID_ACCRUAL_DATA | {
            "period_start": date(2026, 9, 2),
            "period_end": date(2026, 9, 1),
        }

        with pytest.raises(InvalidInterestAccrualPeriodError):
            InterestAccrual(**data)


    @pytest.mark.parametrize(
        "period_start",
        [
            "2026-08-01",
            None,
            123,
        ],
    )
    def test_invalid_period_start_type_is_forbidden(
        self,
        period_start: Any,
    ) -> None:
        data = VALID_ACCRUAL_DATA | {
            "period_start": period_start,
        }

        with pytest.raises(InvalidInterestAccrualPeriodError):
            InterestAccrual(**data)


    @pytest.mark.parametrize(
        "period_end",
        [
            "2026-09-01",
            None,
            123,
        ],
    )
    def test_invalid_period_end_type_is_forbidden(
        self,
        period_end: Any,
    ) -> None:
        data = VALID_ACCRUAL_DATA | {
            "period_end": period_end,
        }

        with pytest.raises(InvalidInterestAccrualPeriodError):
            InterestAccrual(**data)


class TestInterestAccrualFinancialValidation:
    @pytest.mark.parametrize(
        "debt_before",
        [
            Decimal("0.00"),
            Decimal("-1.00"),
            Decimal("NaN"),
            Decimal("Infinity"),
            Decimal("-Infinity"),
            10000,
            10000.0,
            "10000.00",
            None,
        ],
    )
    def test_invalid_debt_before_is_forbidden(
        self,
        debt_before: Any,
    ) -> None:
        data = VALID_ACCRUAL_DATA | {
            "debt_before": debt_before,
        }

        with pytest.raises(InvalidInterestAccrualError):
            InterestAccrual(**data)


    @pytest.mark.parametrize(
        "annual_rate",
        [
            Decimal("-0.01"),
            Decimal("NaN"),
            Decimal("Infinity"),
            Decimal("-Infinity"),
            15,
            15.0,
            "15.00",
            None,
        ],
    )
    def test_invalid_annual_rate_is_forbidden(
        self,
        annual_rate: Any,
    ) -> None:
        data = VALID_ACCRUAL_DATA | {
            "annual_rate": annual_rate,
        }

        with pytest.raises(InvalidInterestAccrualError):
            InterestAccrual(**data)


    def test_zero_annual_rate_is_allowed(self) -> None:
        data = VALID_ACCRUAL_DATA | {
            "annual_rate": Decimal("0.00"),
        }

        accrual = InterestAccrual(**data)

        assert accrual.annual_rate == Decimal("0.00")


    @pytest.mark.parametrize(
        "amount",
        [
            Decimal("0.00"),
            Decimal("-0.01"),
            Decimal("NaN"),
            Decimal("Infinity"),
            Decimal("-Infinity"),
            100,
            100.0,
            "100.00",
            None,
        ],
    )
    def test_invalid_amount_is_forbidden(
        self,
        amount: Any,
    ) -> None:
        data = VALID_ACCRUAL_DATA | {
            "amount": amount,
        }

        with pytest.raises(InvalidInterestAccrualError):
            InterestAccrual(**data)