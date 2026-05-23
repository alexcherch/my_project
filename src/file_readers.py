import pandas as pd


def read_transactions_csv(file_path: str) -> list[dict]:
    """Считывает финансовые операции из CSV-файла и возвращает список словарей."""
    try:
        df = pd.read_csv(file_path)
        # Превращаем DataFrame в список словарей
        transactions: list[dict] = df.to_dict(orient="records")
        return transactions
    except FileNotFoundError:
        print(f"Ошибка: Файл {file_path} не найден.")
        return []
    except Exception as e:
        print(f"Ошибка при чтении CSV: {e}")
        return []


def read_transactions_xlsx(file_path: str) -> list[dict]:
    """Считывает финансовые операции из XLSX-файла и возвращает список словарей."""
    try:
        # Для работы с xlsx используется движок openpyxl
        df = pd.read_excel(file_path, engine="openpyxl")
        transactions: list[dict] = df.to_dict(orient="records")
        return transactions
    except FileNotFoundError:
        print(f"Ошибка: Файл {file_path} не найден.")
        return []
    except Exception as e:
        print(f"Ошибка при чтении XLSX: {e}")
        return []
