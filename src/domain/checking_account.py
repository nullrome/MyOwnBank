from src.domain.balance_account import BalanceAccount

from decimal import Decimal

from src.exceptions import InsufficientFundsError, AccountNotEmptyError


class CheckingAccount(BalanceAccount):
    __slots__ = ()

    def __init__(self, account_id: str, owner: str, balance: Decimal = Decimal("0.00")):
        super().__init__(account_id=account_id, owner=owner, balance=balance)


    def _validate_withdrawal(self, amount: Decimal) -> None:
        if self.balance < amount:
            raise InsufficientFundsError(account_id=self.account_id, balance=self.balance, requested=amount)


    def _validate_closing(self) -> None:
        if self.balance != Decimal("0.00"):
            raise AccountNotEmptyError(balance=self.balance)
