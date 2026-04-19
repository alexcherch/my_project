import pytest

from src.widget import get_date_from_string, mask_account_card


@pytest.fixture
def card_details() -> str:
    """Фикстура для стандартной карты"""
    return "Visa Classic 7000792289606361"


@pytest.fixture
def account_details() -> str:
    """Фикстура для стандартного счета"""
    return "Счет 73654108430135874305"


def test_mask_account_card_visa(card_details: str) -> None:
    """Проверка маскировки карты (Visa)"""
    assert mask_account_card(card_details) == "Visa Classic 7000 79** **** 6361"


def test_mask_account_card_account(account_details: str) -> None:
    """Проверка маскировки счета"""
    assert mask_account_card(account_details) == "Счет **4305"


@pytest.mark.parametrize(
    "user_input, expected",
    [
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("MasterCard 7158300714729458", "MasterCard 7158 30** **** 9458"),
        ("Счет 35384188310052345612", "Счет **5612"),
        ("Visa Gold 5999414289201436", "Visa Gold 5999 41** **** 1436"),
    ],
)
def test_mask_account_card_parametrized(user_input: str, expected: str) -> None:
    """Параметризованный тест для разных типов карт и счетов"""
    assert mask_account_card(user_input) == expected


def test_mask_account_card_invalid_input() -> None:
    """Проверка устойчивости к некорректному вводу (например, отсутствие пробела)"""
    with pytest.raises(ValueError):
        mask_account_card("VisaClassic7000792289606361")


@pytest.mark.parametrize(
    "date_str, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2023-12-31", "31.12.2023"),
        ("Дата операции: 2022-01-01", "01.01.2022"),
    ],
)
def test_get_date_from_string_valid(date_str: str, expected: str) -> None:
    """Проверка корректного преобразования даты"""
    assert get_date_from_string(date_str) == expected


@pytest.mark.parametrize(
    "invalid_date",
    [
        "Нет даты здесь",
        "24-03-11",
        "",
    ],
)
def test_get_date_from_string_missing(invalid_date: str) -> None:
    """Проверка обработки строк без даты или с неверным форматом"""
    assert get_date_from_string(invalid_date) == "Дата не найдена"
