from abc import ABC, abstractmethod
from decimal import Decimal

from src.exceptions import InvalidAmountError, InsufficientFundsError


class BaseAccount(ABC):
    __slots__ = ('__account_id', '__owner', '__balance', '__transaction_history')


    def __init__(self, account_id: str, owner: str, balance: Decimal = Decimal("0.0")):
        self.__account_id = account_id
        self.__owner = owner
        self.__balance = balance


    @property
    def account_id(self) -> str:
        return self.__account_id


    @property
    def owner(self) -> str:
        return self.__owner


    @property
    def balance(self) -> Decimal:
        return self.__balance


    def deposit(self, amount: Decimal):
        if amount <= Decimal("0.0"):
            raise InvalidAmountError(amount)
        self.__balance += amount


    def withdraw(self, amount: Decimal):
        if amount <= Decimal("0.0"):
            raise InvalidAmountError(amount)
        if amount > self.balance:
            raise InsufficientFundsError(account_id=self.account_id,
                                         balance=self.balance,
                                         requested=amount
                                         )
        self._validate_withdrawal(amount)
        self.__balance -= amount


    @abstractmethod
    def _validate_withdrawal(self, amount: Decimal) -> None:
        # heirs return their own verdict
        raise NotImplementedError