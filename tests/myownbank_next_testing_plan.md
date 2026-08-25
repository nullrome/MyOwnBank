# MyOwnBank — план дальнейшего тестирования

> Актуально после полного покрытия миграций `AccountStatus`.

Репозиторий проверен по текущему `main`. Основная реализованная доменная логика сейчас находится в `BaseAccount`, `CheckingAccount` и `SavingsAccount`. `CreditAccount`, `transaction_service`, `interest_service` и `credit_scoring` пока пустые.

## 1. `BaseAccount.deposit()`

- [x] Успешный deposit увеличивает баланс.
- [x] Несколько deposit корректно суммируются.
- [ ] Минимальная положительная `Decimal`-сумма принимается.
- [x] Deposit на `FROZEN` работает согласно текущей реализации.
- [x] После успешного deposit статус не меняется.

### InvalidAmountError

- [x] `Decimal("0.00")`
- [x] отрицательное значение
- [x] `Decimal("NaN")`
- [x] `Decimal("Infinity")`
- [x] `Decimal("-Infinity")`
- [x] `int`
- [x] `float`
- [x] `str`
- [x] `None`

Для каждого:
- [x] баланс не изменился;
- [x] статус не изменился.

### AccountOperationNotAllowedError

- [x] deposit запрещён для `BLOCKED`.
- [x] deposit запрещён для `CLOSED`.
- [x] баланс после ошибки не меняется.

---

## 2. `CheckingAccount.withdraw()`

- [x] Снятие суммы меньше баланса.
- [x] Снятие суммы, равной всему балансу.
- [x] Несколько последовательных снятий.
- [x] Withdraw на `FROZEN` работает согласно текущей реализации.
- [x] После успешного снятия статус не меняется.

### InsufficientFundsError

- [x] Сумма больше баланса.
- [x] Баланс 0, попытка снять положительную сумму.
- [x] Баланс после ошибки не изменился.
- [x] Статус после ошибки не изменился.

### InvalidAmountError

- [x] 0
- [x] отрицательная сумма
- [x] NaN
- [x] Infinity
- [x] -Infinity
- [x] int
- [x] float
- [x] str
- [x] None

### Ограничения статуса

- [x] withdraw запрещён для `BLOCKED`.
- [x] withdraw запрещён для `CLOSED`.
- [x] баланс после ошибки не меняется.

---

## 3. Закрытие `CheckingAccount`

Миграции статусов уже покрыты отдельно. Здесь тестируется финансовый инвариант.

- [x] Нулевой баланс позволяет закрыть счёт.
- [x] Ненулевой баланс вызывает `AccountNotEmptyError`.
- [x] После неудачного close баланс не изменился.
- [x] После неудачного close статус не изменился.
- [x] После снятия остатка до нуля счёт можно закрыть.
- [x] После `deposit() -> withdraw()` до нуля счёт можно закрыть.

---

## 4. Создание и properties `CheckingAccount`

- [x] `account_id` сохраняется.
- [x] `owner` сохраняется.
- [x] `balance` сохраняется как `Decimal`.
- [x] Баланс по умолчанию — `Decimal("0.00")`.
- [x] Properties `account_id`, `owner`, `balance`, `status` возвращают корректные значения.

> Архитектурный вопрос: сейчас `BaseAccount.__init__()` не валидирует initial balance через `_validate_amount()`. Стоит отдельно решить, должны ли отрицательный баланс, `NaN` и `Infinity` быть запрещены при создании счёта, и затем закрепить это тестами.

---

## 5. `SavingsAccount.interest_rate`

### Валидные значения

- [x] `Decimal("0.00")`.
- [x] Положительная ставка.
- [x] Ставка сохраняется корректно.
- [x] Setter меняет валидную ставку на другую валидную.

### InvalidInterestRateError

- [x] отрицательная ставка
- [x] NaN
- [x] Infinity
- [x] -Infinity
- [x] int
- [x] float
- [x] str
- [x] None

Дополнительно:
- [x] после неудачного setter старая ставка остаётся прежней.

---

## 6. Лимит снятий `SavingsAccount`

Текущий лимит: `MAX_WITHDRAWALS_PER_MONTH = 3`.

- [x] Новый Savings имеет `withdrawals_this_month == 0`.
- [x] После 1-го успешного withdraw счётчик == 1.
- [x] После 2-го == 2.
- [x] После 3-го == 3.
- [x] 4-й withdraw вызывает `WithdrawalLimitExceededError`.
- [x] После 4-й неудачной попытки счётчик остаётся 3.
- [x] После 4-й неудачной попытки баланс не меняется.

### Важные edge cases

- [x] `InsufficientFundsError` не увеличивает счётчик.
- [x] `InvalidAmountError` не увеличивает счётчик.
- [x] Ошибка статуса не увеличивает счётчик.
- [x] `deposit()` не влияет на счётчик.

---

## 7. Денежные операции `SavingsAccount`

- [x] Успешный deposit.
- [x] Успешный withdraw.
- [x] Снятие всего баланса.
- [x] `InsufficientFundsError`.
- [x] Невалидные суммы.
- [x] `BLOCKED` запрещает денежные операции.
- [x] `CLOSED` запрещает денежные операции.
- [x] Неудачные операции не меняют баланс.

---

## 8. Закрытие `SavingsAccount`

- [x] Нулевой баланс позволяет закрыть.
- [x] Ненулевой баланс вызывает `AccountNotEmptyError`.
- [x] После ошибки объект не мутирует.
- [x] После снятия остатка до нуля счёт можно закрыть.
- [x] `withdrawals_this_month` не меняется из-за `close()`.

---

## 9. Порядок валидаций

Текущий `withdraw()` идёт примерно так:

```text
status
-> amount
-> account-specific withdrawal rules
-> balance mutation
-> post-withdraw hook
```

Проверить:

- [ ] `BLOCKED` + invalid amount => ошибка статуса.
- [x] `CLOSED` + invalid amount => ошибка статуса.
- [x] `ACTIVE` + invalid amount => `InvalidAmountError`.
- [x] amount > balance => `InsufficientFundsError`.
- [x] Для Savings после достижения лимита зафиксировать тестом приоритет лимита над другими account-specific проверками.

Для `deposit()`:
- [x] `BLOCKED` + invalid amount => сначала ошибка статуса.
- [x] `CLOSED` + invalid amount => сначала ошибка статуса.

---

## 10. Инварианты после исключений

После любой неудачной финансовой операции проверять:

- [x] `balance` не изменился.
- [x] `status` не изменился.
- [x] `withdrawals_this_month` не изменился.
- [x] `interest_rate` не изменился после неудачного setter.

---

## 11. `pytest.mark.parametrize`

После написания базовых тестов вручную параметризовать:

- [x] invalid amounts для deposit.
- [x] invalid amounts для withdraw.
- [x] invalid interest rates.
- [x] операции на `BLOCKED/CLOSED`.

Пример:

```python
@pytest.mark.parametrize(
    "amount",
    [
        Decimal("0.00"),
        Decimal("-1.00"),
        Decimal("NaN"),
        Decimal("Infinity"),
    ],
)
def test_invalid_deposit_amounts_raise_error(amount):
    ...
```

---

## 12. Fixtures

Когда тестов станет много:

- [x] fixture активного `CheckingAccount`.
- [x] fixture пустого `CheckingAccount`.
- [x] fixture `SavingsAccount`.
- [x] не усложнять fixture-зависимости.

---

## 13. Coverage

После покрытия реализованной domain-логики:

- [ ] установить `pytest-cov`;
- [ ] проверить line coverage;
- [ ] проверить branch coverage;
- [ ] посмотреть `term-missing`;
- [ ] закрыть реальные доменные ветки, а не гнаться механически за числом.

Команда:

```bash
pytest --cov=src.domain --cov-branch --cov-report=term-missing
```

---

## Пока НЕ тестировать

На текущем `main` пока пустые:

```text
src/domain/credit_account.py
src/services/transaction_service.py
src/services/interest_service.py
src/services/credit_scoring.py
```

Также `tests/test_api.py` и `tests/test_transactions.py` пока не стоит заполнять искусственными тестами без соответствующей реализации.

- [ ] Реализовать `CreditAccount`.
- [ ] Написать его unit-тесты.
- [ ] Реализовать `TransactionService`.
- [ ] Перейти к `tests/test_transactions.py`.
- [ ] Реализовать `InterestService`.
- [ ] Написать его unit-тесты.
- [ ] Реализовать credit scoring / ML-часть.
- [ ] После появления реального API перейти к `tests/test_api.py`.

---

## Рекомендуемый порядок

```text
DONE: AccountStatus migrations
        ↓
1. BaseAccount.deposit
        ↓
2. CheckingAccount.withdraw
        ↓
3. CheckingAccount.close + invariants
        ↓
4. SavingsAccount.interest_rate
        ↓
5. SavingsAccount withdrawal limit
        ↓
6. SavingsAccount money operations + close
        ↓
7. parametrization + fixtures
        ↓
8. pytest-cov + branch coverage
        ↓
9. CreditAccount implementation + tests
        ↓
10. TransactionService implementation + tests
        ↓
11. InterestService implementation + tests
        ↓
12. API/integration tests
        ↓
13. ML / credit scoring tests
```

---

## Definition of Done перед переходом к Transactions

- [x] Status transitions закрыты.
- [x] `deposit()` полностью покрыт.
- [x] `CheckingAccount.withdraw()` покрыт.
- [x] `CheckingAccount.close()` покрыт.
- [x] `InvalidAmountError` edge cases покрыты.
- [x] `InsufficientFundsError` покрыт.
- [x] `AccountOperationNotAllowedError` покрыт.
- [ ] `SavingsAccount.interest_rate` покрыт.
- [ ] Лимит 3 снятий Savings покрыт.
- [ ] Неудачные операции не мутируют объект.
- [ ] `pytest --cov-branch` не показывает неожиданных дыр в реализованной domain-логике.
- [ ] Все тесты независимы и проходят в любом порядке.
