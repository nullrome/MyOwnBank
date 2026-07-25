from src.domain.base_account import BaseAccount

from decimal import Decimal

from src.exceptions import InsufficientFundsError


class CheckingAccount(BaseAccount):
    __slots__ = ()

    def __init__(self, account_id: str, owner: str, balance: Decimal = Decimal("0.0")):
        super().__init__(account_id=account_id, owner=owner, balance=balance)


    def _validate_withdrawal(self, amount: Decimal) -> None:
        if self.balance < amount:
            raise InsufficientFundsError(account_id=self.account_id, balance=self.balance, requested=amount)
