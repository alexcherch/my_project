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


def get_date(date: str) -> str:
    """Функция, которая принимает на вход строку с полной датой и возвращает строку с датой в формате 'ДД.ММ.ГГГГ'"""
    return date[8:10] + "." + date[5:7] + "." + date[:4]
