from decimal import Decimal
from datetime import date
from uuid import UUID
from dataclasses import dataclass

from src.exceptions import (InvalidInterestAccrualError,
                            InvalidAmountError
                            )


from src.domain.savings.savings_account import SavingsAccount


@dataclass(frozen=True)
class SavingsInterestAccrual:
    accrual_id: UUID
    account_id: str
    accrual_date: date
    amount: Decimal

    def __post_init__(self) -> None:
        self._validate_identifiers(
            accrual_id=self.accrual_id,
            account_id=self.account_id
        )
        self._validate_amount(amount=self.amount)
        self._validate_date(accrual_date=self.accrual_date)


    @staticmethod
    def _validate_identifiers(
            accrual_id: UUID,
            account_id: str
    ) -> None:
        if not isinstance(accrual_id, UUID):
            raise InvalidInterestAccrualError(
                field="accrual_id",
                value=accrual_id
            )
        if not isinstance(account_id, str) or not account_id or account_id != account_id.strip():
            raise InvalidInterestAccrualError(
                field="account_id",
                value=account_id
            )


    @staticmethod
    def _validate_amount(amount: Decimal) -> None:
        if not isinstance(amount, Decimal) or not amount.is_finite() or amount <= Decimal("0.00"):
            raise InvalidAmountError(amount=amount)


    @staticmethod
    def _validate_date(accrual_date: date) -> None:
        if not isinstance(accrual_date, date):
            raise InvalidInterestAccrualError(
                field="date",
                value=accrual_date
            )
