import re

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(user_details: str) -> str:
    """
    Функция принимает информацию о карте или счете
    и возвращает строку с замаскированным номером
    """
    name, number = user_details.rsplit(" ", maxsplit=1)

    if "счет" in name.lower():
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return f"{name} {masked_number}"


def get_date_from_string(date_str: str) -> str:
    """Функция, которая извлекает дату из строки"""
    match = re.search(r"(\d{4})-(\d{2})-(\d{2})", date_str)
    if match:
        year, month, day = match.groups()
        return f"{day}.{month}.{year}"
    return "Дата не найдена"
