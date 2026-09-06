from datetime import date
from decimal import Decimal

from uuid import UUID

from src.exceptions import (
    InvalidInterestAccrualError,
    InvalidInterestAccrualPeriodError,
)


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
        accrual_id: UUID,
        account_id: str,
        period_start: date,
        period_end: date,
        debt_before: Decimal,
        annual_rate: Decimal,
        amount: Decimal,
    ) -> None:
        self._validate_identifiers(
            accrual_id=accrual_id,
            account_id=account_id,
        )
        self._validate_period(
            period_start=period_start,
            period_end=period_end,
        )
        self._validate_financial_data(
            debt_before=debt_before,
            annual_rate=annual_rate,
            amount=amount,
        )

        self.__accrual_id = accrual_id
        self.__account_id = account_id
        self.__period_start = period_start
        self.__period_end = period_end
        self.__debt_before = debt_before
        self.__annual_rate = annual_rate
        self.__amount = amount

    @property
    def accrual_id(self) -> UUID:
        return self.__accrual_id

    @property
    def account_id(self) -> str:
        return self.__account_id

    @property
    def period_start(self) -> date:
        return self.__period_start

    @property
    def period_end(self) -> date:
        return self.__period_end

    @property
    def debt_before(self) -> Decimal:
        return self.__debt_before

    @property
    def annual_rate(self) -> Decimal:
        return self.__annual_rate

    @property
    def amount(self) -> Decimal:
        return self.__amount

    @staticmethod
    def _validate_identifiers(
        accrual_id: UUID,
        account_id: str,
    ) -> None:
        if not isinstance(accrual_id, str) or accrual_id != accrual_id.strip():
            raise InvalidInterestAccrualError(
                field="accrual_id",
                value=accrual_id,
            )

        if not isinstance(account_id, str) or accrual_id != account_id.strip():
            raise InvalidInterestAccrualError(
                field="account_id",
                value=account_id,
            )

    @staticmethod
    def _validate_period(
        period_start: date,
        period_end: date,
    ) -> None:
        if not isinstance(period_start, date):
            raise InvalidInterestAccrualPeriodError(
                period_start=period_start,
                period_end=period_end,
            )

        if not isinstance(period_end, date):
            raise InvalidInterestAccrualPeriodError(
                period_start=period_start,
                period_end=period_end,
            )

        if period_end <= period_start:
            raise InvalidInterestAccrualPeriodError(
                period_start=period_start,
                period_end=period_end,
            )

    @staticmethod
    def _validate_financial_data(
        debt_before: Decimal,
        annual_rate: Decimal,
        amount: Decimal,
    ) -> None:
        if not isinstance(debt_before, Decimal):
            raise InvalidInterestAccrualError(
                field="debt_before",
                value=debt_before,
            )

        if not debt_before.is_finite() or debt_before <= Decimal("0.00"):
            raise InvalidInterestAccrualError(
                field="debt_before",
                value=debt_before,
            )

        if not isinstance(annual_rate, Decimal):
            raise InvalidInterestAccrualError(
                field="annual_rate",
                value=annual_rate,
            )

        if not annual_rate.is_finite() or annual_rate < Decimal("0.00"):
            raise InvalidInterestAccrualError(
                field="annual_rate",
                value=annual_rate,
            )

        if not isinstance(amount, Decimal):
            raise InvalidInterestAccrualError(
                field="amount",
                value=amount,
            )

        if not amount.is_finite() or amount <= Decimal("0.00"):
            raise InvalidInterestAccrualError(
                field="amount",
                value=amount,
            )
