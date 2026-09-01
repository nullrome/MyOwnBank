from abc import ABC, abstractmethod

from decimal import Decimal

from src.domain.account_status import AccountStatus
from domain.accounts.base_account import BaseAccount

from src.exceptions import (AccountOperationNotAllowedError,
                            InvalidAmountError,
                            AccountNotEmptyError
                            )


class BalanceAccount(BaseAccount, ABC):
    __slots__ = "__balance"


    def __init__(
            self,
            account_id: str,
            owner: str,
            balance: Decimal
    ) -> None:
        super().__init__(
            account_id=account_id,
            owner=owner
        )
        self._validate_balance(balance=balance)
        self.__balance = balance


    @property
    def balance(self) -> Decimal:
        return self.__balance


    @abstractmethod
    def _validate_withdrawal(self, amount: Decimal) -> None:
        pass


    @staticmethod
    def _validate_balance(balance: Decimal) -> None:
        if not isinstance(balance, Decimal):
            raise InvalidAmountError(amount=balance)
        if not balance.is_finite():
            raise InvalidAmountError(amount=balance)
        if balance < Decimal("0.00"):
            raise InvalidAmountError(amount=balance)


    def _on_withdrawal(self, amount: Decimal) -> None:
        pass


    def _validate_closing(self) -> None:
        if self.__balance != Decimal("0.00"):
            raise AccountNotEmptyError(balance=self.balance)


    def deposit(self, amount: Decimal) -> None:
        if self.status in (AccountStatus.BLOCKED, AccountStatus.CLOSED):
            raise AccountOperationNotAllowedError(operation="deposit", status=self.status)
        self._validate_amount(amount=amount)
        self.__balance += amount


    def withdraw(self, amount: Decimal) -> None:
        if self.status in (AccountStatus.BLOCKED, AccountStatus.CLOSED):
            raise AccountOperationNotAllowedError(operation="withdraw", status=self.status)
        self._validate_amount(amount=amount)
        self._validate_withdrawal(amount=amount)
        self.__balance -= amount
        self._on_withdrawal(amount=amount)
