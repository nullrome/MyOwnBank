import pytest

from decimal import Decimal

from domain.credit.services.interest_service import calculate_interest

from src.exceptions import (InvalidInterestPeriodError,
                            InvalidInterestRateError,
                            InvalidDebtError)


class TestCalculateInterest:
    def test_calculate_interest_for_debt(self) -> None:
        assert calculate_interest(
            debt=Decimal("10000.00"),
            annual_rate=Decimal("15.00"),
            days=30
        ) == Decimal("123.29")


    def test_calculate_interest_with_zero_debt(self) -> None:
        assert calculate_interest(
            debt=Decimal("0.00"),
            annual_rate=Decimal("15.00"),
            days=30
        ) == Decimal("0.00")


    def test_calculate_interest_with_zero_days(self) -> None:
        assert calculate_interest(
            debt=Decimal("10000.00"),
            annual_rate=Decimal("15.00"),
            days=0
        ) == Decimal("0.00")


    def test_calculate_interest_with_zero_interest_rate(self) -> None:
        assert calculate_interest(
            debt=Decimal("10000.00"),
            annual_rate=Decimal("0.00"),
            days=30
        ) == Decimal("0.00")


class TestCalculateInterestValidation:
    def test_calculate_interest_with_negative_days(self) -> None:
        with pytest.raises(InvalidInterestPeriodError):
            calculate_interest(
                debt=Decimal("10000.00"),
                annual_rate=Decimal("15.00"),
                days=-3
            )


    def test_calculate_interest_with_decimal_days(self) -> None:
        with pytest.raises(InvalidInterestPeriodError):
            calculate_interest(
                debt=Decimal("10000.00"),
                annual_rate=Decimal("15.00"),
                days=Decimal("100.00")
            )


    @pytest.mark.parametrize(
        "invalid_annual_rate",
        [
            Decimal("-1.00"),
            Decimal("Infinity"),
            Decimal("-Infinity"),
            Decimal("NaN"),
            5,
            5.5,
            "Roman",
            None
        ]
    )
    def test_calculate_interest_with_invalid_annual_rate(self, invalid_annual_rate) -> None:
        with pytest.raises(InvalidInterestRateError):
            calculate_interest(
                debt=Decimal("10000.00"),
                annual_rate=invalid_annual_rate,
                days=30
            )


    @pytest.mark.parametrize(
        "invalid_debt",
        [
            Decimal("-1.00"),
            Decimal("Infinity"),
            Decimal("-Infinity"),
            Decimal("NaN"),
            5,
            5.5,
            "Roman",
            None
        ]
    )
    def test_calculate_interest_with_invalid_debt(self, invalid_debt) -> None:
        with pytest.raises(InvalidDebtError):
            calculate_interest(
                debt=invalid_debt,
                annual_rate=Decimal("15.00"),
                days=30
            )


class TestCalculateInterestRounding:
    def test_calculate_simple_interest_rounding(self) -> None:
        assert calculate_interest(
            debt=Decimal("10000.00"),
            annual_rate=Decimal("15.00"),
            days=365
        ) == Decimal("1500.00")


    def test_calculate_complex_interest_rounding(self) -> None:
        assert calculate_interest(
            debt=Decimal("3575.34"),
            annual_rate=Decimal("13.50"),
            days=45
        ) == Decimal("59.51")

