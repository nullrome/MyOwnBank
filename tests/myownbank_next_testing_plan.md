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

- [ ] Нулевой баланс позволяет закрыть счёт.
- [ ] Ненулевой баланс вызывает `AccountNotEmptyError`.
- [ ] После неудачного close баланс не изменился.
- [ ] После неудачного close статус не изменился.
- [ ] После снятия остатка до нуля счёт можно закрыть.
- [ ] После `deposit() -> withdraw()` до нуля счёт можно закрыть.

---

## 4. Создание и properties `CheckingAccount`

- [ ] `account_id` сохраняется.
- [ ] `owner` сохраняется.
- [ ] `balance` сохраняется как `Decimal`.
- [ ] Баланс по умолчанию — `Decimal("0.00")`.
- [ ] Properties `account_id`, `owner`, `balance`, `status` возвращают корректные значения.

> Архитектурный вопрос: сейчас `BaseAccount.__init__()` не валидирует initial balance через `_validate_amount()`. Стоит отдельно решить, должны ли отрицательный баланс, `NaN` и `Infinity` быть запрещены при создании счёта, и затем закрепить это тестами.

---

## 5. `SavingsAccount.interest_rate`

### Валидные значения

- [ ] `Decimal("0.00")`.
- [ ] Положительная ставка.
- [ ] Ставка сохраняется корректно.
- [ ] Setter меняет валидную ставку на другую валидную.

### InvalidInterestRateError

- [ ] отрицательная ставка
- [ ] NaN
- [ ] Infinity
- [ ] -Infinity
- [ ] int
- [ ] float
- [ ] str
- [ ] None

Дополнительно:
- [ ] после неудачного setter старая ставка остаётся прежней.

---

## 6. Лимит снятий `SavingsAccount`

Текущий лимит: `MAX_WITHDRAWALS_PER_MONTH = 3`.

- [ ] Новый Savings имеет `withdrawals_this_month == 0`.
- [ ] После 1-го успешного withdraw счётчик == 1.
- [ ] После 2-го == 2.
- [ ] После 3-го == 3.
- [ ] 4-й withdraw вызывает `WithdrawalLimitExceededError`.
- [ ] После 4-й неудачной попытки счётчик остаётся 3.
- [ ] После 4-й неудачной попытки баланс не меняется.

### Важные edge cases

- [ ] `InsufficientFundsError` не увеличивает счётчик.
- [ ] `InvalidAmountError` не увеличивает счётчик.
- [ ] Ошибка статуса не увеличивает счётчик.
- [ ] `deposit()` не влияет на счётчик.

---

## 7. Денежные операции `SavingsAccount`

- [ ] Успешный deposit.
- [ ] Успешный withdraw.
- [ ] Снятие всего баланса.
- [ ] `InsufficientFundsError`.
- [ ] Невалидные суммы.
- [ ] `BLOCKED` запрещает денежные операции.
- [ ] `CLOSED` запрещает денежные операции.
- [ ] Неудачные операции не меняют баланс.

---

## 8. Закрытие `SavingsAccount`

- [ ] Нулевой баланс позволяет закрыть.
- [ ] Ненулевой баланс вызывает `AccountNotEmptyError`.
- [ ] После ошибки объект не мутирует.
- [ ] После снятия остатка до нуля счёт можно закрыть.
- [ ] `withdrawals_this_month` не меняется из-за `close()`.

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
- [ ] `CLOSED` + invalid amount => ошибка статуса.
- [ ] `ACTIVE` + invalid amount => `InvalidAmountError`.
- [ ] amount > balance => `InsufficientFundsError`.
- [ ] Для Savings после достижения лимита зафиксировать тестом приоритет лимита над другими account-specific проверками.

Для `deposit()`:
- [ ] `BLOCKED` + invalid amount => сначала ошибка статуса.
- [ ] `CLOSED` + invalid amount => сначала ошибка статуса.

---

## 10. Инварианты после исключений

После любой неудачной финансовой операции проверять:

- [ ] `balance` не изменился.
- [ ] `status` не изменился.
- [ ] `withdrawals_this_month` не изменился.
- [ ] `interest_rate` не изменился после неудачного setter.

---

## 11. `pytest.mark.parametrize`

После написания базовых тестов вручную параметризовать:

- [ ] invalid amounts для deposit.
- [ ] invalid amounts для withdraw.
- [ ] invalid interest rates.
- [ ] операции на `BLOCKED/CLOSED`.

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

- [ ] fixture активного `CheckingAccount`.
- [ ] fixture пустого `CheckingAccount`.
- [ ] fixture `SavingsAccount`.
- [ ] не усложнять fixture-зависимости.

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

- [ ] Status transitions закрыты.
- [ ] `deposit()` полностью покрыт.
- [ ] `CheckingAccount.withdraw()` покрыт.
- [ ] `CheckingAccount.close()` покрыт.
- [ ] `InvalidAmountError` edge cases покрыты.
- [ ] `InsufficientFundsError` покрыт.
- [ ] `AccountOperationNotAllowedError` покрыт.
- [ ] `SavingsAccount.interest_rate` покрыт.
- [ ] Лимит 3 снятий Savings покрыт.
- [ ] Неудачные операции не мутируют объект.
- [ ] `pytest --cov-branch` не показывает неожиданных дыр в реализованной domain-логике.
- [ ] Все тесты независимы и проходят в любом порядке.
