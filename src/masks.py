def get_mask_card_number(card_number: int | str) -> str:
    """Функция принимает на вход номер карты в виде числа и возвращает маску номера"""
    card_str = str(card_number).strip()

    if len(card_str) < 13:
        raise ValueError("Номер карты слишком короткий")

    mask_card = card_str[:6] + "******" + card_str[-4:]
    return mask_card[:4] + " " + mask_card[4:8] + " " + mask_card[8:12] + " " + mask_card[12:]


def get_mask_account(account_number: int | str) -> str:
    """Функция принимает на вход номер счета в виде числа и возвращает маску номера"""
    account_str = str(account_number).strip()

    if len(account_str) < 4:
        raise ValueError("Номер счета слишком короткий")

    return "**" + account_str[-4:]
