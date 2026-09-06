from collections.abc import Callable
from uuid import UUID
from decimal import Decimal
from datetime import date

from src.domain.credit.interest_accrual import InterestAccrual
from src.domain.credit.services.interest_service import calculate_interest
from src.domain.credit.credit_account import CreditAccount


def accrue_credit_interest(
        account: CreditAccount,
        period_start: date,
        period_end: date,
        id_generator: Callable[[], UUID]
) -> InterestAccrual | None:

    days = (period_end - period_start).days
    debt_before = account.debt

    interest = calculate_interest(
        debt=account.debt,
        annual_rate=account.interest_rate,
        days=days
    )

    if interest == Decimal("0.00"):
        return None

    account.accrue_interest(interest_amount=interest)

    return InterestAccrual(
        accrual_id=id_generator(),
        account_id=account.account_id,
        period_start=period_start,
        period_end=period_end,
        debt_before=debt_before,
        annual_rate=account.interest_rate,
        amount=interest,
    )


# TODO: replace direct entity passing with repository-based orchestration
# TODO: derive accrual period from dates
# TODO: persist account changes
# TODO: create interest accrual transaction/event