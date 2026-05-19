import json
from typing import Any


def load_transactions(file_path: str) -> list[dict[str, Any]]:
    """Принимает на вход путь до JSON-файла и возвращает список словарей с данными о финансовых транзакциях"""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            return []

    except (FileNotFoundError, json.JSONDecodeError):
        return []
