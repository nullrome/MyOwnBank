from decimal import Decimal

from src.services.interest_service import calculate_interest
from src.domain.credit_account import CreditAccount


def accrue_credit_interest(
        account: CreditAccount,
        days: int
) -> Decimal:
    interest = calculate_interest(
        debt=account.debt,
        annual_rate=account.interest_rate,
        days=days
    )

    if interest > Decimal("0.00"):
        account.accrue_interest(interest_amount=interest)

    return interest


# TODO: replace direct entity passing with repository-based orchestration
# TODO: derive accrual period from dates
# TODO: persist account changes
# TODO: create interest accrual transaction/event
