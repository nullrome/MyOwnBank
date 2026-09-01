from decimal import Decimal, ROUND_HALF_UP

from src.exceptions import (InvalidInterestPeriodError,
                            InvalidInterestRateError,
                            InvalidDebtError)


MONEY_QUANTUM = Decimal("0.01")
DAYS_IN_YEAR = Decimal("365")
PERCENT = Decimal("100")


def _validate_interest_period(days: int) -> None:
    if type(days) is not int or days < 0:
        raise InvalidInterestPeriodError(days=days)


def _validate_annual_rate(annual_rate: Decimal) -> None:
    if not isinstance(annual_rate, Decimal) or not annual_rate.is_finite() or annual_rate < Decimal("0.00"):
        raise InvalidInterestRateError(interest_rate=annual_rate)


def _validate_debt(debt: Decimal) -> None:
    if not isinstance(debt, Decimal) or not debt.is_finite() or debt < Decimal("0.00"):
        raise InvalidDebtError(debt=debt)


def calculate_interest(
        debt: Decimal,
        annual_rate: Decimal,
        days: int
) -> Decimal:
    _validate_debt(debt=debt)
    _validate_annual_rate(annual_rate=annual_rate)
    _validate_interest_period(days=days)
    interest = (
        debt * annual_rate / PERCENT * Decimal(days) / DAYS_IN_YEAR
    )

    return interest.quantize(
        exp=MONEY_QUANTUM,
        rounding=ROUND_HALF_UP
    )