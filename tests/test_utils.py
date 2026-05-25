import json
from unittest.mock import mock_open, patch

import pytest

from src.utils import load_transactions, process_bank_search


def test_load_transactions_success() -> None:
    """Проверка успешного чтения корректного JSON-файла со списком."""
    mock_data = [{"id": 1, "amount": "100.00"}, {"id": 2, "amount": "200.50"}]
    json_string = json.dumps(mock_data)

    with patch("builtins.open", mock_open(read_data=json_string)):
        result = load_transactions("fake_path.json")

    assert result == mock_data
    assert len(result) == 2


def test_load_transactions_file_not_found() -> None:
    """Проверка ситуации, когда файл отсутствует на диске."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = load_transactions("missing_file.json")

    assert result == []


def test_load_transactions_invalid_json() -> None:
    """Проверка ситуации, когда JSON-файл поврежден или пуст."""
    invalid_json = "{ invalid json }"

    with patch("builtins.open", mock_open(read_data=invalid_json)):
        result = load_transactions("bad_file.json")

    assert result == []


def test_load_transactions_not_a_list() -> None:
    """Проверка ситуации, когда JSON валиден, но корневой элемент — не список (например, словарь)."""
    mock_dict = {"status": "error", "message": "not a list"}
    json_string = json.dumps(mock_dict)

    with patch("builtins.open", mock_open(read_data=json_string)):
        result = load_transactions("dict_file.json")

    assert result == []


@pytest.fixture
def sample_transactions() -> list[dict]:
    """Фикстура с тестовыми транзакциями."""
    return [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Оплата услуг"},
        {"id": 3, "description": "перевод частному лицу"},
        {"id": 4, "description": None},
        {"id": 5},
    ]


def test_process_bank_search_success(sample_transactions: list[dict]) -> None:
    """Тест успешного поиска без учета регистра."""
    result = process_bank_search(sample_transactions, "перевод")
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 3


def test_process_bank_search_no_match(sample_transactions: list[dict]) -> None:
    """Тест ситуации, когда совпадений не найдено."""
    result = process_bank_search(sample_transactions, "Снятие наличных")
    assert result == []


def test_process_bank_search_empty_query(sample_transactions: list[dict]) -> None:
    """Тест с пустой строкой поиска (должен вернуть исходный список)."""
    result = process_bank_search(sample_transactions, "")
    assert len(result) == 5
