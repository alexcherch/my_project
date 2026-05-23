from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.file_readers import read_transactions_csv, read_transactions_xlsx


@pytest.fixture
def sample_dataframe() -> pd.DataFrame:
    """Фикстура для создания тестового DataFrame."""
    data = {
        "id": [1, 2],
        "amount": [100.5, -50.0],
        "currency": ["RUB", "USD"],
    }
    return pd.DataFrame(data)


@patch("src.file_readers.pd.read_csv")
def test_read_transactions_csv_success(mock_read_csv: MagicMock, sample_dataframe: pd.DataFrame) -> None:
    """Тест успешного чтения транзакций из CSV."""
    mock_read_csv.return_value = sample_dataframe
    result = read_transactions_csv("fake_path.csv")

    assert len(result) == 2
    assert result[0]["amount"] == 100.5
    assert result[1]["currency"] == "USD"
    mock_read_csv.assert_called_once_with("fake_path.csv")


@patch("src.file_readers.pd.read_csv")
def test_read_transactions_csv_not_found(mock_read_csv: MagicMock) -> None:
    """Тест обработки исключения FileNotFoundError для CSV."""
    mock_read_csv.side_effect = FileNotFoundError
    result = read_transactions_csv("missing.csv")

    assert result == []


@patch("src.file_readers.pd.read_excel")
def test_read_transactions_xlsx_success(mock_read_excel: MagicMock, sample_dataframe: pd.DataFrame) -> None:
    """Тест успешного чтения транзакций из XLSX."""
    mock_read_excel.return_value = sample_dataframe
    result = read_transactions_xlsx("fake_path.xlsx")

    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["amount"] == -50.0
    mock_read_excel.assert_called_once_with("fake_path.xlsx", engine="openpyxl")


@patch("src.file_readers.pd.read_excel")
def test_read_transactions_xlsx_not_found(mock_read_excel: MagicMock) -> None:
    """Тест обработки исключения FileNotFoundError для XLSX."""
    mock_read_excel.side_effect = FileNotFoundError
    result = read_transactions_xlsx("missing.xlsx")

    assert result == []
