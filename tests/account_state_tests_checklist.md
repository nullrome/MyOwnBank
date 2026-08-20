# MyOwnBank — чек-лист тестирования состояний Account

## Правила state machine

Текущие разрешённые переходы:

```text
ACTIVE --freeze()--> FROZEN
ACTIVE --block()----> BLOCKED

FROZEN --activate()-> ACTIVE
FROZEN --block()----> BLOCKED

BLOCKED — конечное состояние
```

Все остальные вызовы методов смены состояния должны завершаться исключением.

---

## Матрица полного покрытия переходов

| Начальное состояние | Метод | Ожидаемый результат |
|---|---|---|
| `ACTIVE` | `activate()` | ❌ исключение |
| `ACTIVE` | `freeze()` | ✅ `FROZEN` |
| `ACTIVE` | `block()` | ✅ `BLOCKED` |
| `FROZEN` | `activate()` | ✅ `ACTIVE` |
| `FROZEN` | `freeze()` | ❌ исключение |
| `FROZEN` | `block()` | ✅ `BLOCKED` |
| `BLOCKED` | `activate()` | ❌ исключение |
| `BLOCKED` | `freeze()` | ❌ исключение |
| `BLOCKED` | `block()` | ❌ исключение |

Итого: **9 базовых сценариев**, из них **4 успешных перехода** и **5 сценариев с исключением**.

---

# 1. Успешные миграции состояний

- [ ] `ACTIVE -> FROZEN`
  - Создать активный аккаунт.
  - Вызвать `account.freeze()`.
  - Проверить `account.status == AccountStatus.FROZEN`.

- [ ] `ACTIVE -> BLOCKED`
  - Создать активный аккаунт.
  - Вызвать `account.block()`.
  - Проверить `account.status == AccountStatus.BLOCKED`.

- [ ] `FROZEN -> ACTIVE`
  - Создать аккаунт.
  - Перевести его в `FROZEN`.
  - Вызвать `account.activate()`.
  - Проверить `account.status == AccountStatus.ACTIVE`.

- [ ] `FROZEN -> BLOCKED`
  - Создать аккаунт.
  - Перевести его в `FROZEN`.
  - Вызвать `account.block()`.
  - Проверить `account.status == AccountStatus.BLOCKED`.

---

# 2. Запрещённые переходы — ожидаем исключение

## Из ACTIVE

- [ ] `ACTIVE -> ACTIVE` через повторный `activate()`
  - Аккаунт уже находится в `ACTIVE`.
  - Вызвать `account.activate()`.
  - Проверить через `pytest.raises(...)`, что выброшено нужное исключение.
  - Проверить, что после исключения статус остался `ACTIVE`.

## Из FROZEN

- [ ] `FROZEN -> FROZEN` через повторный `freeze()`
  - Перевести аккаунт в `FROZEN`.
  - Снова вызвать `account.freeze()`.
  - Проверить выброс нужного исключения.
  - Проверить, что статус остался `FROZEN`.

## Из BLOCKED

- [ ] `BLOCKED -> ACTIVE`
  - Перевести аккаунт в `BLOCKED`.
  - Вызвать `account.activate()`.
  - Проверить выброс нужного исключения.
  - Проверить, что статус остался `BLOCKED`.

- [ ] `BLOCKED -> FROZEN`
  - Перевести аккаунт в `BLOCKED`.
  - Вызвать `account.freeze()`.
  - Проверить выброс нужного исключения.
  - Проверить, что статус остался `BLOCKED`.

- [ ] `BLOCKED -> BLOCKED` через повторный `block()`
  - Перевести аккаунт в `BLOCKED`.
  - Снова вызвать `account.block()`.
  - Проверить выброс нужного исключения.
  - Проверить, что статус остался `BLOCKED`.

---

# 3. Что проверять в каждом exception-тесте

Для каждого запрещённого перехода желательно проверить не только сам факт ошибки.

- [ ] Выбрасывается **конкретный тип исключения**, а не просто любой `Exception`.
- [ ] Исключение возникает именно на вызове метода смены состояния.
- [ ] После исключения `account.status` **не изменился**.
- [ ] Если у исключения есть важное сообщение — проверить его содержимое.
- [ ] Если используется собственное доменное исключение, проверить именно его.

Пример структуры:

```python
def test_blocked_account_cannot_be_activated():
    account = CheckingAccount(
        account_id="1",
        owner="Roman",
        balance=Decimal("1000.00"),
    )

    account.block()

    with pytest.raises(YourException):
        account.activate()

    assert account.status == AccountStatus.BLOCKED
```

> `YourException` нужно заменить на конкретное исключение, которое используется в проекте.

---

# 4. Проверка цепочек переходов

Эти тесты немного пересекаются с базовыми переходами, но проверяют поведение state machine как последовательности операций.

- [ ] `ACTIVE -> FROZEN -> ACTIVE`
  - `freeze()`
  - `activate()`
  - итоговый статус `ACTIVE`.

- [ ] `ACTIVE -> FROZEN -> BLOCKED`
  - `freeze()`
  - `block()`
  - итоговый статус `BLOCKED`.

- [ ] `ACTIVE -> FROZEN -> ACTIVE -> BLOCKED`
  - `freeze()`
  - `activate()`
  - `block()`
  - итоговый статус `BLOCKED`.

- [ ] После `ACTIVE -> BLOCKED` невозможно выполнить `activate()`.

- [ ] После `ACTIVE -> BLOCKED` невозможно выполнить `freeze()`.

- [ ] После `ACTIVE -> FROZEN -> BLOCKED` невозможно выполнить `activate()`.

- [ ] После `ACTIVE -> FROZEN -> BLOCKED` невозможно выполнить `freeze()`.

---

# 5. Инвариант BLOCKED

`BLOCKED` в текущей модели является terminal state.

- [ ] Из `BLOCKED` нельзя перейти в `ACTIVE`.
- [ ] Из `BLOCKED` нельзя перейти в `FROZEN`.
- [ ] Повторный вызов `block()` запрещён.
- [ ] После любой неудачной попытки изменить `BLOCKED` статус остаётся `BLOCKED`.

---

# 6. Итоговый Definition of Done

Смена состояний аккаунта считается полностью покрытой базовыми unit-тестами, когда:

- [ ] Проверены все **4 разрешённых перехода**.
- [ ] Проверены все **5 запрещённых вызовов**.
- [ ] Каждый запрещённый вызов проверяет конкретный тип исключения.
- [ ] После каждого исключения проверяется неизменность состояния.
- [ ] Проверено, что `BLOCKED` является terminal state.
- [ ] Проверены основные последовательности из нескольких переходов.
- [ ] Все тесты проходят через `pytest`.
- [ ] Нет тестов, которые зависят от порядка запуска других тестов.

---

## Минимальный набор для 100% покрытия таблицы переходов

```text
[x] ACTIVE  + activate() = exception
[x] ACTIVE  + freeze()   = FROZEN
[x] ACTIVE  + block()    = BLOCKED

[x] FROZEN  + activate() = ACTIVE
[x] FROZEN  + freeze()   = exception
[x] FROZEN  + block()    = BLOCKED

[x] BLOCKED + activate() = exception
[x] BLOCKED + freeze()   = exception
[x] BLOCKED + block()    = exception
```

Это именно **100% покрытие матрицы переходов состояний**, а не утверждение о 100% `line/branch coverage` всего класса `Account`.
