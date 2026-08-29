import pytest

from decimal import Decimal

from src.services.interest_service import calculate_interest


class TestCalculateInterest:
    def test_calculates_interest_for_debt(self) -> None:
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


