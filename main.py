import os
from typing import Any

from src.file_readers import read_transactions_csv, read_transactions_xlsx
from src.generators import filter_by_currency
from src.processing import filter_by_state, sort_by_date
from src.utils import load_transactions, process_bank_search
from src.widget import get_date_from_string, mask_account_card


def normalize_transaction_structure(tx: dict[str, Any]) -> dict[str, Any]:
    """Приводит плоскую структуру CSV/XLSX (включая склеенные через ';' строки) к стандарту JSON."""
    if "operationAmount" in tx and isinstance(tx["operationAmount"], dict):
        return tx

    if len(tx) == 1 and ";" in list(tx.keys())[0]:
        raw_key = list(tx.keys())[0]
        raw_value = str(list(tx.values())[0])
        headers = raw_key.split(";")
        values = raw_value.split(";")
        while len(values) < len(headers):
            values.append("")
        tx = dict(zip(headers, values))

    amount = tx.get("amount", "0")
    currency_code = tx.get("currency_code", "RUB")
    currency_name = tx.get("currency_name", "руб.")

    if isinstance(amount, float):
        amount = int(amount) if amount.is_integer() else amount

    raw_state = tx.get("state")
    state_str = str(raw_state).strip().upper() if raw_state and str(raw_state) != "nan" else ""

    from_field = tx.get("from")
    to_field = tx.get("to")

    from_str = (
        "" if (not from_field or (isinstance(from_field, float) and str(from_field) == "nan")) else str(from_field)
    )
    to_str = "" if (not to_field or (isinstance(to_field, float) and str(to_field) == "nan")) else str(to_field)

    new_tx = {
        "id": tx.get("id"),
        "state": state_str,
        "date": tx.get("date"),
        "description": tx.get("description"),
        "from": from_str,
        "to": to_str,
        "operationAmount": {"amount": str(amount), "currency": {"name": currency_name, "code": currency_code}},
    }
    return new_tx


def main() -> None:
    """Основная функция, управляющая логикой и связывающая функциональности проекта."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    transactions: list[dict[str, Any]] = []

    while True:
        choice = input("Пользователь: ").strip()
        if choice == "1":
            print("\nПрограмма: Для обработки выбран JSON-файл.")
            path = os.path.join(current_dir, "data", "operations.json")
            transactions = load_transactions(path)
            break
        elif choice == "2":
            print("\nПрограмма: Для обработки выбран CSV-файл.")
            path = os.path.join(current_dir, "data", "transactions.csv")
            transactions = read_transactions_csv(path)
            break
        elif choice == "3":
            print("\nПрограмма: Для обработки выбран XLSX-файл.")
            path = os.path.join(current_dir, "data", "transactions_excel.xlsx")
            transactions = read_transactions_xlsx(path)
            break
        else:
            print("Программа: Некорректный пункт меню. Пожалуйста, выберите 1, 2 или 3.")

    transactions = [normalize_transaction_structure(tx) for tx in transactions]

    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        print("\nПрограмма: Введите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")
        status_input = input("Пользователь: ").strip()
        status_upper = status_input.upper()

        if status_upper in valid_statuses:
            transactions = filter_by_state(transactions, status_upper)
            print(f'\nПрограмма: Операции отфильтрованы по статусу "{status_upper}"')
            break
        else:
            print(f'\nПрограмма: Статус операции "{status_input}" недоступен.')

    print("\nПрограмма: Отсортировать операции по дате? Да/Нет")
    confirm_sort = input("Пользователь: ").strip().lower()

    if confirm_sort == "да":
        while True:
            print("\nПрограмма: Отсортировать по возрастанию или по убыванию?")
            sort_direction = input("Пользователь: ").strip().lower()

            if "возрастанию" in sort_direction:
                transactions = sort_by_date(transactions, ascending=False)
                break
            elif "убыванию" in sort_direction:
                transactions = sort_by_date(transactions, ascending=True)
                break
            else:
                print("Программа: Пожалуйста, введите 'по возрастанию' или 'по убыванию'.")

    print("\nПрограмма: Выводить только рублевые транзакции? Да/Нет")
    confirm_rub = input("Пользователь: ").strip().lower()

    if confirm_rub == "да":
        transactions = list(filter_by_currency(transactions, "RUB"))

    print("\nПрограмма: Отфильтровать список транзакций по определенному слову в описании? Да/Нет")
    confirm_search = input("Пользователь: ").strip().lower()

    if confirm_search == "да":
        search_query = input("Пользователь (слово для поиска): ").strip()
        transactions = process_bank_search(transactions, search_query)

    print("\nПрограмма: Распечатываю итоговый список транзакций...\n")

    if not transactions:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"Программа: Всего банковских операций в выборке: {len(transactions)}\n")

    for tx in transactions:
        raw_date = tx.get("date", "")
        formatted_date = get_date_from_string(raw_date) if raw_date else "Дата не найдена"
        description = tx.get("description", "Без описания")

        from_info = tx.get("from", "")
        to_info = tx.get("to", "")

        masked_from = mask_account_card(from_info) if from_info else ""
        masked_to = mask_account_card(to_info) if to_info else "Не указан"

        if masked_from:
            direction = f"{masked_from} -> {masked_to}"
        else:
            direction = masked_to

        amount = tx["operationAmount"]["amount"]
        currency = tx["operationAmount"]["currency"]["name"]

        print(f"{formatted_date} {description}")
        if direction:
            print(direction)
        print(f"Сумма: {amount} {currency}\n")


if __name__ == "__main__":
    main()
