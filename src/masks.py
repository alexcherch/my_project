import logging

logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("logs/masks.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")

file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: int | str) -> str:
    """Функция принимает на вход номер карты в виде числа и возвращает маску номера"""
    card_str = str(card_number).strip()

    if len(card_str) < 13:
        logger.error(f"Ошибка маскирования: Номер карты слишком короткий ({card_number})")
        raise ValueError("Номер карты слишком короткий")

    mask_card = card_str[:6] + "******" + card_str[-4:]
    result = mask_card[:4] + " " + mask_card[4:8] + " " + mask_card[8:12] + " " + mask_card[12:]
    logger.info(f"Успешно замаскирован номер карты: {result}")
    return result


def get_mask_account(account_number: int | str) -> str:
    """Функция принимает на вход номер счета в виде числа и возвращает маску номера"""
    account_str = str(account_number).strip()

    if len(account_str) < 4:
        logger.error(f"Ошибка маскирования: Номер счета слишком короткий ({account_number})")
        raise ValueError("Номер счета слишком короткий")

    result = "**" + account_str[-4:]
    logger.info(f"Успешно замаскирован номер счета: {result}")
    return result
