from functools import wraps
from typing import Callable, Any


def log(filename: str | None = None) -> Callable:
    """
    Декоратор, который логирует начало и результат выполнения функции,
    в том числе ошибки.

    :param filename: Путь к файлу лога. Если None, вывод идет в консоль.
    :return: Декорированная функция с поддержкой логирования.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            log_message = ""

            start_msg = f"{func.__name__} started"

            def write_log(msg: str) -> None:
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(msg + "\n")
                else:
                    print(msg)

            write_log(start_msg)

            try:
                result = func(*args, **kwargs)
                log_message = f"{func.__name__} ok"
                return result
            except Exception as e:
                error_type = type(e).__name__
                log_message = f"{func.__name__} error: {error_type}. Inputs: {args}, {kwargs}"
                raise
            finally:
                if log_message:
                    write_log(log_message)

        return wrapper

    return decorator
