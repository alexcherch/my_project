from typing import Any, Iterator


def filter_by_currency(transactions: list[dict[str, Any]], currency_code: str) -> Iterator[dict[str, Any]]:
    """Фильтрует транзакции по заданному коду валюты"""
    for transaction in transactions:
        if transaction["operationAmount"]["currency"]["code"] == currency_code:
            yield transaction


def transaction_descriptions(transactions: list[dict[str, Any]]) -> Iterator[str]:
    """Возвращает описание каждой транзакции по очереди"""
    for transaction in transactions:
        yield transaction["description"]


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """Генерирует номера карт в формате XXXX XXXX XXXX XXXX"""
    for number in range(start, stop + 1):
        card_str = f"{number:016}"
        formatted_card = f"{card_str[:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:]}"
        yield formatted_card
