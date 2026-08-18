from enum import StrEnum


class AccountStatus(StrEnum):
    ACTIVE = "active"
    FROZEN = "frozen"
    BLOCKED = "blocked"
    CLOSED = "closed"