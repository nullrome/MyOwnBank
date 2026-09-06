from collections.abc import Callable
from uuid import UUID
from datetime import date

import pytest

from decimal import Decimal

from src.domain.credit.interest_accrual import InterestAccrual
from src.application.credit.use_cases.accrue_credit_interest import accrue_credit_interest
from src.domain.credit.credit_account import CreditAccount


CreditAccountFactory = Callable[..., CreditAccount]


FIXED_ACCRUAL_ID = UUID("12345678-1234-5678-1234-567812345678")


def fixed_uuid_generator() -> UUID:
    return FIXED_ACCRUAL_ID


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


class TestAccrueCreditInterest:
    def test_accrue_calculated_interest_to_account(
            self,
            credit_account_factory: CreditAccountFactory,
    ) -> None:
        account = credit_account_factory()
        account.spend(Decimal("1000.00"))

        accrual = accrue_credit_interest(
            account=account,
            period_start=date(2026, 8, 1),
            period_end=date(2026, 8, 31),
            id_generator=fixed_uuid_generator,
        )

        assert isinstance(accrual, InterestAccrual)
        assert accrual.accrual_id == FIXED_ACCRUAL_ID
        assert accrual.account_id == account.account_id
        assert accrual.debt_before == Decimal("1000.00")
        assert accrual.amount == Decimal("12.33")
        assert account.debt == Decimal("1012.33")


    def test_accrue_credit_interest_with_zero_debt(
            self,
            credit_account_factory: CreditAccountFactory
    ) -> None:
        account = credit_account_factory()
        result = accrue_credit_interest(
            account=account,
            period_start=date(2026, 8, 1),
            period_end=date(2026, 8, 31),
            id_generator=fixed_uuid_generator,
        )

        assert result is None
        assert account.debt == Decimal("0.00")


    def test_accrue_credit_interest_with_zero_interest_rate(
            self,
            credit_account_factory: CreditAccountFactory
    ) -> None:
        account = credit_account_factory(interest_rate=Decimal("0.00"))

        account.spend(Decimal("1000.00"))

        interest = accrue_credit_interest(
            account=account,
            period_start=date(2026, 8, 1),
            period_end=date(2026, 9, 1),
            id_generator=fixed_uuid_generator
        )

        assert interest is None
        assert account.debt == Decimal("1000.00")


    def test_accrue_credit_interest_with_zero_days(
            self,
            credit_account_factory: CreditAccountFactory
    ) -> None:
        account = credit_account_factory()

        account.spend(Decimal("1000.00"))

        interest = accrue_credit_interest(
            account=account,
            period_start=date(2026, 8, 1),
            period_end = date(2026, 8, 1),
            id_generator=fixed_uuid_generator
        )

        assert interest is None
        assert account.debt == Decimal("1000.00")
