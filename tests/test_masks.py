import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.fixture
def card_number_standard() -> str:
    """Возвращает стандартный номер карты для базовых проверок."""
    return "7000792289606361"


def test_get_mask_card_number_format(card_number_standard: str) -> None:
    """Проверяет правильность маскирования на эталонном примере."""
    assert get_mask_card_number(card_number_standard) == "7000 79** **** 6361"


@pytest.mark.parametrize(
    "card_input, expected_output",
    [
        (1234567812345678, "1234 56** **** 5678"),
        ("1111222233334444", "1111 22** **** 4444"),
    ],
)
def test_get_mask_card_number_types(card_input: int | str, expected_output: int | str) -> None:
    """Проверяет работу с разными типами входных данных (int/str)."""
    assert get_mask_card_number(card_input) == expected_output


@pytest.mark.parametrize("invalid_input", ["123", ""])
def test_get_mask_card_number_errors(invalid_input: str) -> None:
    """Проверяет реакцию на некорректную длину номера."""
    with pytest.raises(ValueError, match="Номер карты слишком короткий"):
        get_mask_card_number(invalid_input)


@pytest.fixture
def account_number_standard() -> str:
    """Фикстура для стандартного номера счета"""
    return "73654108430135874305"


def test_get_mask_account_format(account_number_standard: str) -> None:
    """Проверка маскирования стандартного номера"""
    assert get_mask_account(account_number_standard) == "**4305"


@pytest.mark.parametrize(
    "account_input, expected_output",
    [
        (73654108430135874305, "**4305"),  # Тип int
        ("99998888777766665555", "**5555"),  # Тип str
        ("4305", "**4305"),  # Граничное значение (ровно 4 цифры)
    ],
)
def test_get_mask_account_variations(account_input: int | str, expected_output: int | str) -> None:
    """Проверка различных длин и типов данных"""
    assert get_mask_account(account_input) == expected_output


@pytest.mark.parametrize(
    "invalid_input",
    [
        "123",  # Меньше 4 символов
        "",  # Пустая строка
    ],
)
def test_get_mask_account_errors(invalid_input: str) -> None:
    """Проверка реакции на критически короткие номера"""
    with pytest.raises(ValueError, match="Номер счета слишком короткий"):
        get_mask_account(invalid_input)
