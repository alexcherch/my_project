import json
from typing import Any
from unittest.mock import mock_open, patch

from src.utils import load_transactions, process_bank_operations, process_bank_search


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


def test_process_bank_search_success() -> None:
    """Тест успешного поиска без учета регистра."""
    sample_data = [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Оплата услуг"},
        {"id": 3, "description": "перевод частному лицу"},
    ]
    result = process_bank_search(sample_data, "перевод")
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 3


def test_process_bank_search_empty_query() -> None:
    """Тест с пустой строкой поиска (должен вернуть исходный список)."""
    sample_data = [{"id": 1, "description": "Перевод организации"}]
    result = process_bank_search(sample_data, "")
    assert result == sample_data


def test_process_bank_operations_success() -> None:
    """Тест успешного подсчета операций по категориям."""
    sample_data: list[dict[str, Any]] = [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Оплата услуг связи"},
        {"id": 3, "description": "перевод частному лицу"},
        {"id": 4, "description": "Покупка продуктов"},
        {"id": 5, "description": None},
    ]
    categories = ["Перевод", "Оплата услуг", "Снятие наличных"]

    result = process_bank_operations(sample_data, categories)

    assert result["Перевод"] == 2
    assert result["Оплата услуг"] == 1
    assert result["Снятие наличных"] == 0


def test_process_bank_operations_empty_data() -> None:
    """Тест подсчета при пустом списке транзакций."""
    categories = ["Перевод"]
    result = process_bank_operations([], categories)
    assert result == {"Перевод": 0}
