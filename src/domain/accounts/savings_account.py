from domain.accounts.balance_account import BalanceAccount

from decimal import Decimal

from src.exceptions import (InvalidInterestRateError,
                            WithdrawalLimitExceededError,
                            InsufficientFundsError,
                            AccountNotEmptyError
                            )


class SavingsAccount(BalanceAccount):
    __slots__ = ('__interest_rate', '__withdrawal_this_month')

    MAX_WITHDRAWALS_PER_MONTH = 3

    def __init__(self,
                 account_id: str,
                 owner: str,
                 interest_rate: Decimal,
                 balance: Decimal = Decimal("0.00")
        ) -> None:
        super().__init__(account_id=account_id, owner=owner, balance=balance)
        self.interest_rate = interest_rate
        self.__withdrawal_this_month = 0


    @property
    def withdrawals_this_month(self) -> int:
        return self.__withdrawal_this_month


    @property
    def interest_rate(self) -> Decimal:
        return self.__interest_rate


    @interest_rate.setter
    def interest_rate(self, interest_rate: Decimal) -> None:
        if not isinstance(interest_rate, Decimal):
            raise InvalidInterestRateError(interest_rate=interest_rate)
        if not interest_rate.is_finite():
            raise InvalidInterestRateError(interest_rate=interest_rate)
        if interest_rate <= Decimal("0.00"):
            raise InvalidInterestRateError(interest_rate=interest_rate)
        self.__interest_rate = interest_rate


    def _validate_withdrawal(self, amount: Decimal) -> None:
        if self.__withdrawal_this_month >= self.MAX_WITHDRAWALS_PER_MONTH:
            raise WithdrawalLimitExceededError(owner=self.owner, withdrawals_this_month=self.withdrawals_this_month)
        if self.balance < amount:
            raise InsufficientFundsError(account_id=self.account_id, balance=self.balance, requested=amount)


    def _validate_closing(self) -> None:
        if self.balance != Decimal("0.00"):
            raise AccountNotEmptyError(balance=self.balance)


    def _on_withdrawal(self, amount: Decimal) -> None:
        self.__withdrawal_this_month += 1