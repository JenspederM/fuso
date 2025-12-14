"""Utility functions for Fuso.

Includes functions for merging dictionaries and lists of dictionaries,
sorting, and converting between different data structures.
"""


def to_list_of_dicts_by_key(values: list, key: str = "name") -> dict:
    """Convert a list of dictionaries to a dictionary of dictionaries
        using a specified key.

    Args:
        values (list): List of dictionaries to convert
        key (str): Key to use as the dictionary key

    Returns:
        dict: Dictionary of dictionaries

    Example:
        ```py
        values = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
        ]
        assert to_list_of_dicts_by_key(values, "name") == {
            "Alice": {"age": 30},
            "Bob": {"age": 25},
        }
        assert to_list_of_dicts_by_key(values, "age") == {
            30: {"name": "Alice"},
            25: {"name": "Bob"},
        }
        ```
    """
    result = {}
    for value in values:
        value_copy = value.copy()
        try:
            value_key = value_copy.pop(key)
            result[value_key] = value_copy
        except KeyError:
            all_keys = ", ".join(value.keys())
            raise KeyError(
                f"Key '{key}' not found in value. Available keys: {all_keys}"
            )
    return result


def sort_list_of_dicts_by_key(
    values: list[dict], key: str, reverse: bool = False
) -> list[dict]:
    """Sort a list of dictionaries by a specified key.

    Args:
        values (list[dict]): List of dictionaries to sort
        key (str): Key to sort by
        reverse (bool): Whether to sort in descending order

    Returns:
        list[dict]: Sorted list of dictionaries

    Example:
        ```py
        values = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
        ]
        assert sort_list_of_dicts_by_key(values, key="age") == [
            {"name": "Bob", "age": 25},
            {"name": "Alice", "age": 30},
        ]
        assert sort_list_of_dicts_by_key(values, key="age", reverse=True) == [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
        ]
        ```
    """
    return sorted(values, key=lambda x: x[key], reverse=reverse)


def sort_dict(d: dict, key_order: list[str] | None = None) -> dict:
    """Sort a dictionary by a given (non-exhaustive) key order.

    Args:
        d (dict): dictionary to sort
        key_order (list[str]): Non-exhaustive list of keys to sort by

    Returns:
        dict: dictionary with ordered values

    Example:
        ```py
        d = {
            "b": 2,
            "a": 1,
            "c": 3,
        }
        assert sort_dict(d, key_order=["a", "b"]) == {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        assert sort_dict(d) == {
            "b": 2,
            "a": 1,
            "c": 3,
        }
        ```
    """
    if key_order is None:
        key_order = []
    other_keys = [k for k in d.keys() if k not in key_order]
    order = key_order + other_keys
    return dict(sorted(d.items(), key=lambda x: order.index(x[0])))
