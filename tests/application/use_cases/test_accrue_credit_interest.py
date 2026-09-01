from collections.abc import Callable

import pytest

from decimal import Decimal

from src.application.use_cases.accrue_credit_interest import accrue_credit_interest
from src.domain.credit_account import CreditAccount


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


class TestAccrueCreditInterest:
    def test_accrue_calculated_interest_to_account(
            self,
            credit_account_factory: CreditAccountFactory
    ) -> None:
        account = credit_account_factory()
        account.spend(Decimal("1000.00"))

        interest = accrue_credit_interest(
            account=account,
            days=30
        )

        assert interest == Decimal("12.33")
        assert account.debt == Decimal("1012.33")