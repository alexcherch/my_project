from unittest.mock import MagicMock, patch

from src.external_api import get_transaction_amount


def test_get_transaction_amount_rub() -> None:
    """Проверка для транзакции в рублях. Запрос к API происходить не должен."""
    transaction = {"operationAmount": {"amount": "31957.58", "currency": {"code": "RUB"}}}
    assert get_transaction_amount(transaction) == 31957.58


@patch("src.external_api.requests.get")
@patch("src.external_api.API_KEY", "fake_api_key")
def test_get_transaction_amount_usd_success(mock_get: MagicMock) -> None:
    """Проверка успешного ответа от API при конвертации USD."""
    transaction = {"operationAmount": {"amount": "100.00", "currency": {"code": "USD"}}}

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 7500.888}
    mock_get.return_value = mock_response

    result = get_transaction_amount(transaction)

    assert result == 7500.89
    mock_get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/convert",
        headers={"apikey": "fake_api_key"},
        params={"from": "USD", "to": "RUB", "amount": 100.00},
        timeout=10,
    )


@patch("src.external_api.requests.get")
@patch("src.external_api.API_KEY", "fake_api_key")
def test_get_transaction_amount_api_error(mock_get: MagicMock) -> None:
    """Проверка ситуации, когда сервер API вернул ошибку (например, 403 или 500)."""
    transaction = {"operationAmount": {"amount": "50.00", "currency": {"code": "EUR"}}}

    mock_response = MagicMock()
    mock_response.status_code = 403
    mock_response.text = "Forbidden"
    import requests

    mock_response.raise_for_status.side_effect = requests.HTTPError()
    mock_get.return_value = mock_response

    assert get_transaction_amount(transaction) == 0.0


def test_get_transaction_amount_invalid_data() -> None:
    """Проверка ситуации, когда в словаре транзакции отсутствуют нужные ключи."""
    assert get_transaction_amount({}) == 0.0

    bad_transaction = {"operationAmount": {"currency": {"code": "USD"}}}
    assert get_transaction_amount(bad_transaction) == 0.0
