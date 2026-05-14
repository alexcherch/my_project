import os

from src.external_api import get_transaction_amount
from src.utils import load_transactions


def main() -> None:
    root_dir = os.path.dirname(os.path.abspath(__file__))
    path_to_json = os.path.join(root_dir, "data", "operations.json")

    print("--- Шаг 1: Загрузка транзакций ---")
    transactions = load_transactions(path_to_json)
    print(f"Успешно загружено транзакций из файла: {len(transactions)}\n")

    if not transactions:
        print("Список транзакций пуст. Проверьте файл operations.json.")
        return

    print("--- Шаг 2: Проверка обработки транзакций ---")
    for index, tx in enumerate(transactions[:3], start=1):
        print(f"Транзакция №{index} (ID: {tx.get('id')})")

        currency = tx.get("operationAmount", {}).get("currency", {}).get("code", "???")
        amount_init = tx.get("operationAmount", {}).get("amount", "0")
        print(f"  Исходная сумма: {amount_init} {currency}")

        amount_in_rub = get_transaction_amount(tx)
        print(f"  Результат функции в RUB: {amount_in_rub}")
        print("-" * 40)


if __name__ == "__main__":
    main()
