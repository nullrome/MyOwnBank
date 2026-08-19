from abc import ABC, abstractmethod

from decimal import Decimal

from src.exceptions import InvalidAmountError, InvalidAccountStatusTransitionError, AccountOperationNotAllowedError

from src.domain.account_status import AccountStatus


class BaseAccount(ABC):
    __slots__ = ('__account_id', '__owner', '__balance', '__transaction_history', '__status')


    def __init__(self, account_id: str, owner: str, balance: Decimal = Decimal("0.00")):
        self.__account_id = account_id
        self.__owner = owner
        self.__balance = balance
        self.__status = AccountStatus.ACTIVE


    @property
    def account_id(self) -> str:
        return self.__account_id


    @property
    def owner(self) -> str:
        return self.__owner


    @property
    def balance(self) -> Decimal:
        return self.__balance


    @property
    def status(self) -> AccountStatus:
        return self.__status


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


    def _validate_amount(self, amount: Decimal) -> None:
        if not isinstance(amount, Decimal):
            raise InvalidAmountError(amount=amount)
        if not amount.is_finite():
            raise InvalidAmountError(amount=amount)
        if amount <= Decimal("0.00"):
            raise InvalidAmountError(amount=amount)


    @abstractmethod
    def _validate_withdrawal(self, amount: Decimal) -> None:
        # heirs return their own
        raise NotImplementedError


    @abstractmethod
    def _validate_closing(self) -> None:
        pass


    def _on_withdrawal(self, amount: Decimal) -> None:
        # heirs do their own actions
        pass


    def freeze(self) -> None:
        if self.__status in (AccountStatus.ACTIVE, AccountStatus.BLOCKED):
            self.__status = AccountStatus.FROZEN
            return
        raise InvalidAccountStatusTransitionError(self.__status, AccountStatus.FROZEN)


    def block(self) -> None:
        if self.__status in (AccountStatus.ACTIVE, AccountStatus.FROZEN):
            self.__status = AccountStatus.BLOCKED
            return
        raise InvalidAccountStatusTransitionError(self.__status, AccountStatus.BLOCKED)


    def activate(self) -> None:
        if self.__status in (AccountStatus.BLOCKED, AccountStatus.FROZEN):
            self.__status = AccountStatus.ACTIVE
            return
        raise InvalidAccountStatusTransitionError(self.__status, AccountStatus.ACTIVE)


    def close(self) -> None:
        if self.__status == AccountStatus.BLOCKED:
            raise InvalidAccountStatusTransitionError(self.__status, AccountStatus.BLOCKED)
        self._validate_closing()
        self.__status = AccountStatus.CLOSED
