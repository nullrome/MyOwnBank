from decimal import Decimal, ROUND_HALF_UP


MONEY_QUANTUM = Decimal("0.01")
DAYS_IN_YEAR = Decimal("365")
PERCENT = Decimal("100")


def calculate_interest(
        debt: Decimal,
        annual_rate: Decimal,
        days: int
) -> Decimal:
    interest = (
        debt * annual_rate / PERCENT * Decimal(days) / DAYS_IN_YEAR
    )

    return interest.quantize(
        exp=MONEY_QUANTUM,
        rounding=ROUND_HALF_UP
    )