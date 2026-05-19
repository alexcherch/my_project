import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
URL_CONVERT = "https://api.apilayer.com/exchangerates_data/convert"


def get_transaction_amount(transaction: dict) -> float:
    """Принимает словарь транзакции и возвращает сумму в рублях (float).
    Если валюта отличается от RUB, делает запрос к API для конвертации.
    """
    operation_amount = transaction.get("operationAmount", {})
    amount_str = operation_amount.get("amount")
    currency = operation_amount.get("currency", {}).get("code")

    if not amount_str or not currency:
        return 0.0

    amount = float(amount_str)

    if currency == "RUB":
        return amount

    if not API_KEY:
        raise ValueError("API_KEY не найден в переменных окружения")

    headers: dict[str, str | bytes] = {"apikey": API_KEY}
    payload = {"from": currency, "to": "RUB", "amount": amount}

    try:
        response = requests.get(URL_CONVERT, headers=headers, params=payload, timeout=10)

        if response.status_code != 200:
            print(f"Ошибка API! Статус: {response.status_code}, Ответ: {response.text}")

        response.raise_for_status()
        data = response.json()

        raw_result = float(data.get("result", 0.0))
        return round(raw_result, 2)

    except (requests.RequestException, ValueError, KeyError):
        return 0.0
