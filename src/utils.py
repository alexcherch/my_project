import json
import logging
import re
from collections import Counter
from typing import Any

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("logs/utils.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")

file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def load_transactions(file_path: str) -> list[dict[str, Any]]:
    """Принимает на вход путь до JSON-файла и возвращает список словарей с данными о финансовых транзакциях"""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                logger.info(f"Успешно загружено транзакций из файла: {file_path}")
                return data
            logger.warning(f"Файл {file_path} содержит JSON, но это не список")
            return []

    except FileNotFoundError:
        logger.error(f"Файл не найден по пути: {file_path}")
        return []

    except json.JSONDecodeError:
        logger.error(f"Ошибка декодирования JSON в файле: {file_path}")
        return []


def process_bank_search(data: list[dict[str, Any]], search: str) -> list[dict[str, Any]]:
    """Фильтрует список транзакций по строке поиска в описании (description)."""
    if not search:
        logger.info("Передана пустая строка поиска. Возвращен исходный список.")
        return data

    try:
        pattern = re.compile(re.escape(search), re.IGNORECASE)
    except Exception as e:
        logger.error(f"Ошибка компиляции регулярного выражения для '{search}': {e}")
        return []

    filtered_data: list[dict[str, Any]] = []
    for transaction in data:
        description = transaction.get("description")
        if isinstance(description, str) and pattern.search(description):
            filtered_data.append(transaction)

    logger.info(f"Поиск по запросу '{search}' успешно завершен. Найдено совпадений: {len(filtered_data)}")
    return filtered_data


def process_bank_operations(data: list[dict[str, Any]], categories: list[str]) -> dict[str, int]:
    """Подсчитывает количество операций для каждой заданной категории в поле description."""
    logger.info(f"Начало подсчета операций по {len(categories)} категориям.")
    found_categories: list[str] = []

    for transaction in data:
        description = transaction.get("description")
        if not isinstance(description, str):
            continue

        for category in categories:
            if re.search(re.escape(category), description, re.IGNORECASE):
                found_categories.append(category)

    counts = dict(Counter(found_categories))

    result = {category: counts.get(category, 0) for category in categories}

    logger.info("Подсчет операций успешно завершен.")
    return result
