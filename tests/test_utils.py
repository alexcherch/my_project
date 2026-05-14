import json
from unittest.mock import mock_open, patch

from src.utils import load_transactions


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
