from typing import Any

import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def sample_data() -> list[dict[str, Any]]:
    """Фикстура с эталонным набором транзакций"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-03-11T02:00:00"},
        {"id": 2, "state": "CANCELED", "date": "2023-12-15T15:00:00"},
        {"id": 3, "state": "EXECUTED", "date": "2024-01-01T00:00:00"},
        {"id": 4, "state": "PENDING", "date": "2024-01-01T00:00:00"},
    ]


@pytest.mark.parametrize(
    "state_param, expected_count",
    [
        ("EXECUTED", 2),
        ("CANCELED", 1),
        ("PENDING", 1),
        ("NON_EXISTENT", 0),
    ],
)
def test_filter_by_state(sample_data: list[dict[str, Any]], state_param: str, expected_count: int) -> None:
    """Проверка фильтрации по разным статусам"""
    result = filter_by_state(sample_data, state_param)
    assert len(result) == expected_count
    for item in result:
        assert item["state"] == state_param


def test_filter_by_state_empty_list() -> None:
    """Проверка работы с пустым списком"""
    assert filter_by_state([], "EXECUTED") == []


def test_sort_by_date_default_descending(sample_data: list[dict[str, Any]]) -> None:
    """Проверка сортировки по убыванию (по умолчанию в коде reverse=False, т.е. возрастание)"""
    result = sort_by_date(sample_data)
    assert [item["id"] for item in result] == [2, 3, 4, 1]


def test_sort_by_date_ascending(sample_data: list[dict[str, Any]]) -> None:
    """Проверка сортировки по возрастанию (когда ascending=True -> reverse=True)"""
    result = sort_by_date(sample_data, ascending=True)
    assert [item["id"] for item in result] == [1, 3, 4, 2]


def test_sort_by_date_same_dates(sample_data: list[dict[str, Any]]) -> None:
    """Проверка корректности сортировки при одинаковых датах"""
    result = sort_by_date(sample_data, ascending=True)
    assert result[1]["date"] == result[2]["date"]


@pytest.mark.parametrize(
    "bad_data",
    [
        ([{"id": 1, "date": "not-a-date"}]),
        ([{"id": 1, "date": "2024-13-45"}]),
    ],
)
def test_sort_by_date_invalid_formats(bad_data: list[dict[str, Any]]) -> None:
    """Тест на работу с некорректными форматами строк"""
    result = sort_by_date(bad_data)
    assert result == bad_data
