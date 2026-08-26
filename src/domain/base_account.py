from abc import ABC, abstractmethod

from decimal import Decimal

from src.exceptions import InvalidAmountError, InvalidAccountStatusTransitionError

from src.domain.account_status import AccountStatus


class BaseAccount(ABC):
    __slots__ = ('__account_id', '__owner', '__status')


    def __init__(
            self,
            account_id: str,
            owner: str
    ) -> None:
        self.__account_id = account_id
        self.__owner = owner
        self.__status = AccountStatus.ACTIVE


    @property
    def account_id(self) -> str:
        return self.__account_id


    @property
    def owner(self) -> str:
        return self.__owner


    @property
    def status(self) -> AccountStatus:
        return self.__status


    @abstractmethod
    def _validate_closing(self) -> None:
        pass


    def freeze(self) -> None:
        if self.__status == AccountStatus.ACTIVE:
            self.__status = AccountStatus.FROZEN
            return
        raise InvalidAccountStatusTransitionError(self.__status, AccountStatus.FROZEN)


    def block(self) -> None:
        if self.__status in (AccountStatus.ACTIVE, AccountStatus.FROZEN):
            self.__status = AccountStatus.BLOCKED
            return
        raise InvalidAccountStatusTransitionError(self.__status, AccountStatus.BLOCKED)


    def activate(self) -> None:
        if self.__status == AccountStatus.FROZEN:
            self.__status = AccountStatus.ACTIVE
            return
        raise InvalidAccountStatusTransitionError(self.__status, AccountStatus.ACTIVE)


    def close(self) -> None:
        if self.__status == AccountStatus.BLOCKED:
            raise InvalidAccountStatusTransitionError(self.__status, AccountStatus.BLOCKED)
        self._validate_closing()
        self.__status = AccountStatus.CLOSED
