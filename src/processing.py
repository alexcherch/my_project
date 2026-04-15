def filter_by_state(list_of_states: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Фильтрует список словарей по значению state"""
    filtered_list = []

    for item in list_of_states:
        if item.get("state") == state:
            filtered_list.append(item)

    return filtered_list


def sort_by_date(list_of_dates: list[dict], ascending: bool = False) -> list[dict]:
    """Сортирует список словарей по дате."""
    sorted_list = sorted(list_of_dates, key=lambda item: item["date"], reverse=ascending)

    return sorted_list
