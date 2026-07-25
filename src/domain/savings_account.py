from src.domain.base_account import BaseAccount

from decimal import Decimal

from src.exceptions import *


class SavingsAccount(BaseAccount):
    __slots__ = ('__interest_rate', '__withdrawal_this_month')

    MAX_WITHDRAWALS_PER_MONTH = 3

    def __init__(self,
                 account_id: str,
                 owner: str,
                 interest_rate: Decimal,
                 balance: Decimal = Decimal('0.0')
        ) -> None:
        super().__init__(account_id=account_id, owner=owner, balance=balance)
        if not isinstance(interest_rate, Decimal) or interest_rate < Decimal('0.0'):
            raise InvalidAmountError(interest_rate)
        self.__interest_rate = interest_rate
        self.__withdrawal_this_month = 0


    @property
    def interest_rate(self) -> Decimal:
        return self.__interest_rate


    @interest_rate.setter
    def interest_rate(self, interest_rate):
        if interest_rate < 0:
            raise InvalidInterestRateError(interest_rate)


    def _validate_withdrawal(self, amount: Decimal) -> None:
        if not self.__withdrawal_this_month >= self.MAX_WITHDRAWALS_PER_MONTH:
            raise WithdrawalLimitExceededError()
        if not isinstance(amount, Decimal):
            raise InsufficientFundsError(account_id=self.account_id, balance=self.balance, requested=amount)
