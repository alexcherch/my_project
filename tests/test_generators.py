from typing import Any

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def transactions_list() -> list[dict[str, Any]]:
    """Фикстура с тестовыми данными транзакций"""
    return [
        {"id": 939719570, "operationAmount": {"currency": {"code": "USD"}}, "description": "Перевод организации"},
        {"id": 142264268, "operationAmount": {"currency": {"code": "USD"}}, "description": "Перевод со счета на счет"},
        {"id": 873106923, "operationAmount": {"currency": {"code": "RUB"}}, "description": "Перевод со счета на счет"},
        {"id": 895315941, "operationAmount": {"currency": {"code": "USD"}}, "description": "Перевод с карты на карту"},
        {"id": 594226727, "operationAmount": {"currency": {"code": "RUB"}}, "description": "Перевод организации"},
    ]


def test_filter_by_currency_standard(transactions_list: list[dict[str, Any]]) -> None:
    """Проверка корректной фильтрации по заданной валюте"""
    usd_gen = filter_by_currency(transactions_list, "USD")
    results = list(usd_gen)
    assert len(results) == 3
    for trans in results:
        assert trans["operationAmount"]["currency"]["code"] == "USD"


def test_filter_by_currency_no_match(transactions_list: list[dict[str, Any]]) -> None:
    """Проверка случая, когда транзакции в заданной валюте отсутствуют"""
    eur_gen = filter_by_currency(transactions_list, "EUR")
    assert list(eur_gen) == []


def test_filter_by_currency_empty_input() -> None:
    """Проверка работы с пустым списком"""
    assert list(filter_by_currency([], "USD")) == []


def test_transaction_descriptions_logic(transactions_list: list[dict[str, Any]]) -> None:
    """Проверка возврата корректных описаний для каждой транзакции"""
    descriptions = list(transaction_descriptions(transactions_list))
    assert len(descriptions) == len(transactions_list)
    assert descriptions[0] == "Перевод организации"
    assert descriptions[3] == "Перевод с карты на карту"


def test_transaction_descriptions_empty() -> None:
    """Проверка работы с различным количеством данных, включая пустой список"""
    assert list(transaction_descriptions([])) == []


@pytest.mark.parametrize(
    "start, stop, expected_count",
    [(1, 5, 5), (10, 10, 1), (100, 105, 6)],  # Обычный диапазон  # Крайний случай: старт равен стоп  # Другой диапазон
)
def test_card_number_generator_range(start: int, stop: int, expected_count: int) -> None:
    """Проверка выдачи правильных номеров в заданном диапазоне."""
    numbers = list(card_number_generator(start, stop))
    assert len(numbers) == expected_count


def test_card_number_generator_formatting() -> None:
    """Проверка корректности форматирования и завершения генерации."""
    gen = card_number_generator(1, 1)
    card = next(gen)
    # Проверка формата XXXX XXXX XXXX XXXX (16 цифр + 3 пробела = 19 символов)
    assert len(card) == 19
    assert card[4] == " " and card[9] == " " and card[14] == " "
    assert card.replace(" ", "").isdigit()

    # Проверка завершения генерации
    with pytest.raises(StopIteration):
        next(gen)
