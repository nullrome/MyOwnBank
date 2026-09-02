from datetime import date
from decimal import Decimal


class InterestAccrual:
    __slots__ = (
        "__accrual_id",
        "__account_id",
        "__period_start",
        "__period_end",
        "__debt_before",
        "__annual_rate",
        "__amount",
    )

    def __init__(
            self,
            accrual_id: str,
            account_id: str,
            period_start: date,
            period_end: date,
            debt_before: Decimal,
            annual_rate: Decimal,
            amount: Decimal,
    ) -> None:
        ...