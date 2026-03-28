import re

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(card_or_account_number: str) -> str:
    """Функция, которая принимает строку, содержащую тип и номер карты или счета,
    и возвращает строку с замаскированным номером"""
    splits = card_or_account_number.split()
    new_splits = []
    for split in splits:
        if split.isdigit():
            if len(split) == 16:
                new_splits.append(get_mask_card_number(split))
            else:
                new_splits.append(get_mask_account(split))
        else:
            new_splits.append(split)
    return " ".join(new_splits)


# def mask_account_card(user_details: str) -> str:
#     """
#     Функция принимает информацию о карте или счете
#     и возвращает строку с замаскированным номером
#     """
#     account_type, number = user_details.rsplit(" ", maxsplit=1)
#
#     if account_type == "Счет":
#         masked_number = get_mask_account(number)
#     else:
#         masked_number = get_mask_card_number(number)
#
#     return f"{account_type} {masked_number}"


# def get_date(date: str) -> str:
#     """Функция, которая принимает на вход строку с полной датой и возвращает строку с датой в формате 'ДД.ММ.ГГГГ'"""
#     return date[8:10] + "." + date[5:7] + "." + date[:4]


def get_date_from_string(date_str: str) -> str:
    """Функция, которая извлекает дату из строки"""
    match = re.search(r"(\d{4})-(\d{2})-(\d{2})", date_str)
    if match:
        year, month, day = match.groups()
        return f"{day}.{month}.{year}"
    return "Дата не найдена"
