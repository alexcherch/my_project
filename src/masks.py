def get_mask_card_number(card_number: int | str) -> str:
    """Функция принимает на вход номер карты в виде числа и возвращает маску номера"""
    card_str = str(card_number)
    mask_card = card_str[:6] + "******" + card_str[12:]
    return mask_card[:4] + " " + mask_card[4:8] + " " + mask_card[8:12] + " " + mask_card[12:]


def get_mask_account(account_number: int | str) -> str:
    """Функция принимает на вход номер счета в виде числа и возвращает маску номера"""
    account_str = str(account_number)
    return "**" + account_str[-4:]
