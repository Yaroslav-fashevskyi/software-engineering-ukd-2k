# Практична робота — рефакторинг із патернами (Python)

Реалізовано Factory Method, Strategy та Adapter за навчальними завданнями, з демонстрацією коду **до** та **після** рефакторингу. Для Python 3.10+; зовнішні пакети не потрібні.

## Структура

- `src/before/` — початкові версії з додаванням функціональності через умовні оператори.
- `src/after/` — кінцеві версії за патернами з додатковими вимогами: Markdown + CSV, поштомат, CryptoPay.
- `tests/test_patterns.py` — модульні перевірки.
- `results/` — журнали реального запуску, отримані локально.

## Запуск

```bash
python src/after/factory_method.py
python src/after/strategy.py
python src/after/adapter.py
python -m unittest discover -s tests -v
```

## Пояснення

**Factory Method**: абстрактний `InvoiceProcessingService.create_exporter()` повертає один із `InvoiceExporter` за вибором конкретного сервісу. Додано Markdown і CSV, не змінюючи базовий сервіс.

**Strategy**: `OrderShippingContext` приймає `ShippingStrategy` та змінює алгоритм розрахунку через `set_strategy`. Додано `PostMachineStrategy`: 50 грн, обмеження до 10 кг включно.

**Adapter**: `CheckoutService` працює через `PaymentProcessor.pay`. Адаптери для навчальних GlobalPaySDK та CryptoPayService переводять несумісні інтерфейси в спільний контракт. Платіжні SDK — *імітації*; код не виконує реальних оплат.

## Реальне використання патернів

1. Strategy — Tenacity: стратегії очікування `wait_fixed`, `wait_exponential` у [`tenacity/wait.py`](https://github.com/jd/tenacity/blob/main/tenacity/wait.py). Приклад використання в [документації](https://github.com/jd/tenacity/blob/main/doc/source/index.rst).
2. Adapter — Requests: `BaseAdapter` та `HTTPAdapter`, що надають єдиний інтерфейс для HTTP-транспорту в [`requests/adapters.py`](https://github.com/psf/requests/blob/main/src/requests/adapters.py).

Файли звіту — окремо від коду, у DOCX (відкривається Google Docs).
