from decimal import Decimal

from src.exceptions import (InvalidCreditLimitError,
                            InvalidInterestRateError,
                            OutstandingDebtError,
                            CreditLimitExceededError,
                            AccountOperationNotAllowedError,
                            RepaymentExceedsDebtError
                            )

from src.domain.base_account import BaseAccount
from src.domain.account_status import AccountStatus


class CreditAccount(BaseAccount):
    __slots__ = ("__credit_limit",
                 "__debt",
                 "__interest_rate"
                )

    def __init__(
            self,
            account_id: str,
            owner: str,
            credit_limit: Decimal,
            interest_rate: Decimal
            ) -> None:
        super().__init__(
            account_id=account_id,
            owner=owner
        )
        self._validate_credit_limit(credit_limit=credit_limit)
        self.__credit_limit = credit_limit

        self._validate_interest_rate(interest_rate=interest_rate)
        self.__interest_rate = interest_rate
        self.__debt = Decimal("0.00")


    @property
    def credit_limit(self) -> Decimal:
        return self.__credit_limit


    @property
    def interest_rate(self) -> Decimal:
        return self.__interest_rate


    @property
    def debt(self) -> Decimal:
        return self.__debt


    @property
    def available_credit(self) -> Decimal:
        return self.__credit_limit - self.__debt


    @staticmethod
    def _validate_credit_limit(credit_limit: Decimal) -> None:
        if not isinstance(credit_limit, Decimal):
            raise InvalidCreditLimitError(credit_limit=credit_limit)

        if not credit_limit.is_finite():
            raise InvalidCreditLimitError(credit_limit=credit_limit)

        if credit_limit <= Decimal("0.00"):
            raise InvalidCreditLimitError(credit_limit=credit_limit)


    @staticmethod
    def _validate_interest_rate(interest_rate: Decimal) -> None:
        if not isinstance(interest_rate, Decimal):
            raise InvalidInterestRateError(interest_rate=interest_rate)

        if not interest_rate.is_finite():
            raise InvalidInterestRateError(interest_rate=interest_rate)

        if interest_rate < Decimal("0.00"):
            raise InvalidInterestRateError(interest_rate=interest_rate)


    def _validate_spending(self, spending_amount: Decimal) -> None:
        if self.status != AccountStatus.ACTIVE:
            raise AccountOperationNotAllowedError(
                operation="spending",
                status=self.status
                )

        self._validate_amount(amount=spending_amount)

        if spending_amount > self.available_credit:
            raise CreditLimitExceededError(
                                        amount=spending_amount,
                                        available_credit=self.available_credit
                                        )


    def _validate_repayment(self, repayment_amount: Decimal) -> None:
        if self.status not in (AccountStatus.ACTIVE, AccountStatus.FROZEN):
            raise AccountOperationNotAllowedError(
                operation="repayment",
                status=self.status
            )

        self._validate_amount(amount=repayment_amount)

        if repayment_amount > self.__debt:
            raise RepaymentExceedsDebtError(
                amount=repayment_amount,
                debt=self.__debt
            )


    def spend(self, spending_amount: Decimal) -> None:
        self._validate_spending(spending_amount=spending_amount)
        self.__debt += spending_amount


    def repay(self, repayment_amount: Decimal) -> None:
        self._validate_repayment(repayment_amount=repayment_amount)
        self.__debt -= repayment_amount


    def _validate_closing(self) -> None:
        if self.__debt > Decimal("0.00"):
            raise OutstandingDebtError(debt=self.__debt)

