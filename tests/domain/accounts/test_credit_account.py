from collections.abc import Callable

import pytest

from decimal import Decimal

from src.exceptions import (InvalidCreditLimitError,
                            InvalidInterestRateError,
                            CreditLimitExceededError,
                            InvalidAmountError,
                            AccountOperationNotAllowedError,
                            OutstandingDebtError,
                            RepaymentExceedsDebtError)

from src.domain.account_status import AccountStatus
from src.domain.credit.credit_account import CreditAccount


CreditAccountFactory = Callable[..., CreditAccount]


@pytest.fixture
def credit_account_factory() -> CreditAccountFactory:
    def _create(
            credit_limit: Decimal = Decimal("10000.00"),
            interest_rate: Decimal = Decimal("15.00")
    ) -> CreditAccount:
        return CreditAccount(
            account_id="credit-1",
            owner="Roman",
            credit_limit=credit_limit,
            interest_rate=interest_rate
        )
    return _create


class TestCreditAccountCreation:
    def test_attempt_to_set_valid_credit_limit_and_interest_rate(
            self,
            credit_account_factory: CreditAccountFactory
    ) -> None:
        account = credit_account_factory(
            credit_limit=Decimal("10000.00"),
            interest_rate=Decimal("15.00")
        )

        assert account.credit_limit == Decimal("10000.00")
        assert account.interest_rate == Decimal("15.00")
        assert account.status == AccountStatus.ACTIVE


    @pytest.mark.parametrize(
        "invalid_credit_limit",
        [
            Decimal("0.00"),
            Decimal("-1.00"),
            Decimal("NaN"),
            Decimal("Infinity"),
            Decimal("-Infinity"),
            5,
            5.5,
            "Roman",
            None
        ]
    )
    def test_attempt_to_set_invalid_credit_limit(
            self,
            invalid_credit_limit,
            credit_account_factory: CreditAccountFactory
            ) -> None:

        with pytest.raises(InvalidCreditLimitError):
            account = credit_account_factory(
                credit_limit=invalid_credit_limit,
                interest_rate=Decimal("15.00")
            )


    @pytest.mark.parametrize(
        "invalid_interest_rate",
        [
            Decimal("-1.00"),
            Decimal("NaN"),
            Decimal("Infinity"),
            Decimal("-Infinity"),
            5,
            5.5,
            "Roman",
            None
        ]
    )
    def test_attempt_to_set_invalid_interest_rate(
            self,
            invalid_interest_rate,
            credit_account_factory: CreditAccountFactory
    ) -> None:

        with pytest.raises(InvalidInterestRateError):
            account = credit_account_factory(
                credit_limit=Decimal("100000.00"),
                interest_rate=invalid_interest_rate
        )


class TestCreditAccountProperties:
    def test_properties_work_correctly(self, credit_account_factory) -> None:
        account = credit_account_factory(
            credit_limit=Decimal("10000.00"),
            interest_rate=Decimal("15.00")
        )

        assert account.credit_limit == Decimal("10000.00")
        assert account.interest_rate == Decimal("15.00")
        assert account.account_id == "credit-1"
        assert account.owner == "Roman"
        assert account.debt == Decimal("0.00")
        assert account.available_credit == Decimal("10000.00")
        assert account.status == AccountStatus.ACTIVE


class TestCreditAccountSpending:
    def test_spend_less_and_equal_to_limit_amount(self, credit_account_factory) -> None:
        account = credit_account_factory(
            credit_limit=Decimal("100000.00"),
            interest_rate=Decimal("15.00")
        )
        account.spend(Decimal("50000.00"))

        assert account.available_credit == Decimal("50000.00")
        assert account.debt == Decimal("50000.00")

        account.spend(Decimal("50000.00"))

        assert account.available_credit == Decimal("0.00")
        assert account.debt == Decimal("100000.00")


    def test_attempt_to_spend_more_than_possible(self, credit_account_factory) -> None:
        account = credit_account_factory(
            credit_limit=Decimal("100000.00"),
            interest_rate=Decimal("15.00")
        )

        with pytest.raises(CreditLimitExceededError):
            account.spend(Decimal("150000.00"))

        assert account.debt == Decimal("0.00")
        assert account.available_credit == Decimal("100000.00")


    @pytest.mark.parametrize(
        "invalid_spending_amount",
        [
            Decimal("0.00"),
            Decimal("-1.00"),
            Decimal("NaN"),
            Decimal("Infinity"),
            Decimal("-Infinity"),
            5,
            5.5,
            "Roman",
            None
        ]
    )
    def test_attempt_to_spend_invalid_amount(self, invalid_spending_amount, credit_account_factory) -> None:
        account = credit_account_factory(
            credit_limit=Decimal("100000.00"),
            interest_rate=Decimal("15.00")
        )

        with pytest.raises(InvalidAmountError):
            account.spend(invalid_spending_amount)

        assert account.available_credit == Decimal("100000.00")
        assert account.debt == Decimal("0.00")
        assert account.status == AccountStatus.ACTIVE


    def test_frozen_account_cannot_spend(self, credit_account_factory) -> None:
        account = credit_account_factory(
            credit_limit=Decimal("100000.00"),
            interest_rate=Decimal("15.00")
        )

        account.freeze()

        with pytest.raises(AccountOperationNotAllowedError):
            account.spend(Decimal("100.00"))

        assert account.status == AccountStatus.FROZEN


    def test_blocked_account_cannot_spend(self, credit_account_factory) -> None:
        account = credit_account_factory(
            credit_limit=Decimal("100000.00"),
            interest_rate=Decimal("15.00")
        )

        account.block()

        with pytest.raises(AccountOperationNotAllowedError):
            account.spend(Decimal("100.00"))

        assert account.status == AccountStatus.BLOCKED


    def test_closed_account_cannot_spend(self, credit_account_factory) -> None:
        account = credit_account_factory(
            credit_limit=Decimal("100000.00"),
            interest_rate=Decimal("15.00")
        )

        account.close()

        with pytest.raises(AccountOperationNotAllowedError):
            account.spend(Decimal("100.00"))

        assert account.status == AccountStatus.CLOSED


class TestCreditAccountRepayment:
    def test_attempt_to_repay_valid_amount(self, credit_account_factory) -> None:
        account = credit_account_factory()
        account.spend(Decimal("5000.00"))

        assert account.debt == Decimal("5000.00")

        account.repay(Decimal("5000.00"))

        assert account.debt == Decimal("0.00")
        assert account.available_credit == Decimal("10000.00")


    def test_attempt_to_repay_more_than_necessary(self, credit_account_factory) -> None:
        account = credit_account_factory()

        account.spend(Decimal("5000.00"))

        with pytest.raises(RepaymentExceedsDebtError):
            account.repay(Decimal("10000.00"))

        assert account.debt == Decimal("5000.00")
        assert account.available_credit == Decimal("5000.00")


    @pytest.mark.parametrize(
        "invalid_repayment_amount",
        [
            Decimal("0.00"),
            Decimal("-1.00"),
            Decimal("NaN"),
            Decimal("Infinity"),
            Decimal("-Infinity"),
            5,
            5.5,
            "Roman",
            None
        ]
    )
    def test_attempt_to_repay_invalid_amount(self, credit_account_factory, invalid_repayment_amount) -> None:
        account = credit_account_factory()

        account.spend(Decimal("5000.00"))

        with pytest.raises(InvalidAmountError):
            account.repay(invalid_repayment_amount)

        assert account.debt == Decimal("5000.00")


    def test_frozen_account_can_repay(self, credit_account_factory) -> None:
        account = credit_account_factory()
        account.spend(Decimal("5000.00"))

        account.freeze()

        account.repay(Decimal("5000.00"))

        assert account.debt == Decimal("0.00")
        assert account.status == AccountStatus.FROZEN


    def test_blocked_account_cannot_repay(self, credit_account_factory) -> None:
        account = credit_account_factory()
        account.spend(Decimal("5000.00"))

        account.block()

        with pytest.raises(AccountOperationNotAllowedError):
            account.repay(Decimal("5000.00"))


    def test_closed_account_cannot_repay(self, credit_account_factory) -> None:
        account = credit_account_factory()

        account.close()

        with pytest.raises(AccountOperationNotAllowedError):
            account.repay(Decimal("5000.00"))


class TestAccrueInterest:
    def test_interest_can_be_accrued(self, credit_account_factory: CreditAccountFactory) -> None:
        account = credit_account_factory()
        account.spend(Decimal("1000.00"))

        account.accrue_interest(Decimal("15.00"))

        assert account.debt == Decimal("1015.00")


    def test_frozen_account_can_accrue_interest(self, credit_account_factory: CreditAccountFactory) -> None:
        account = credit_account_factory()
        account.spend(Decimal("1000.00"))

        account.freeze()

        account.accrue_interest(Decimal("15.00"))

        assert account.debt == Decimal("1015.00")
        assert account.status == AccountStatus.FROZEN


    def test_blocked_account_can_accrue_interest(self, credit_account_factory: CreditAccountFactory) -> None:
        account = credit_account_factory()
        account.spend(Decimal("1000.00"))

        account.block()

        account.accrue_interest(Decimal("15.00"))

        assert account.debt == Decimal("1015.00")
        assert account.status == AccountStatus.BLOCKED

    def test_closed_account_cannot_accrue_interest(self, credit_account_factory: CreditAccountFactory) -> None:
        account = credit_account_factory()

        account.close()

        with pytest.raises(AccountOperationNotAllowedError):
            account.accrue_interest(Decimal("15.00"))

        assert account.status == AccountStatus.CLOSED


    def test_available_credit_not_less_than_zero(self) -> None:
        account = CreditAccount(
            account_id="credit-1",
            owner="Roman",
            credit_limit=Decimal("1000.00"),
            interest_rate=Decimal("10.00")
        )

        account.spend(Decimal("950.00"))
        account.accrue_interest(Decimal("100.00"))

        assert account.debt == Decimal("1050.00")
        assert account.credit_limit == Decimal("1000.00")
        assert account.available_credit == Decimal("0.00")


class TestCreditAccountClosing:
    def test_account_with_debt_cannot_be_closed(self, credit_account_factory) -> None:
        account = credit_account_factory(
            credit_limit=Decimal("100000.00"),
            interest_rate=Decimal("15.00")
        )

        account.spend(Decimal("50000.00"))

        with pytest.raises(OutstandingDebtError):
            account.close()

        assert account.debt == Decimal("50000.00")
        assert account.available_credit == Decimal("50000.00")
        assert account.status == AccountStatus.ACTIVE


    def test_attempt_to_close_account_without_debt(self, credit_account_factory) -> None:
        account = credit_account_factory()

        account.close()

        assert account.status == AccountStatus.CLOSED
        assert account.debt == Decimal("0.00")
