from collections.abc import Callable
from typing import Any

from fuso.dicts import merge_dict
from fuso.utils import sort_list_of_dicts_by_key, to_list_of_dicts_by_key


def merge_list_of_dicts_by_key(  # noqa: PLR0913 - Too many arguments, but they are all necessary for the functionality
    values: list[dict],
    updates: list[dict],
    key: str,
    default_key: str | None = None,
    merge_functions: dict[str, Callable[[Any, Any], Any]] | None = None,
    object_key_order: list[str] | None = None,
) -> list[dict]:
    """Merge two lists of dictionaries by a specified key.

    Args:
        values (list[dict]): List of original dictionaries
        updates (list[dict]): List of dictionaries with updates
        key (str): Key to use for merging
        default_key (str | None): Key to use for default updates
        merge_functions (dict[str, Callable[[Any, Any], Any]] | None):
            Dictionary of functions to use for merging specific keys
        object_key_order (list[str] | None): Non-exhaustive list of keys to sort objects
            by

    Returns:
        list[dict]: Merged list of dictionaries

    Example:
        ```py
        values = [
            {"id": 1, "name": "Alice", "tags": ["user"]},
            {"id": 2, "name": "Bob", "tags": ["admin"]},
        ]
        updates = [
            {"id": 1, "tags": ["editor"]},
            {"id": 3, "name": "Charlie", "tags": ["user"]},
        ]
        merged = merge_list_of_dicts_by_key(values, updates, key="id")
        assert merged == [
            {"id": 1, "name": "Alice", "tags": ["user", "editor"]},
            {"id": 2, "name": "Bob", "tags": ["admin"]},
            {"id": 3, "name": "Charlie", "tags": ["user"]},
        ]
        ```
    """
    if merge_functions is None:
        merge_functions = {}
    dict_values = to_list_of_dicts_by_key(values or [], key=key)
    try:
        dict_updates = to_list_of_dicts_by_key(updates or [], key=key)
    except KeyError as e:
        raise KeyError(
            f"Key '{key}' not found in update. Available keys: "
            f"{', '.join(updates[0].keys())}"
        ) from e
    if default_key is not None:
        default_updates = dict_updates.pop(default_key, {})
    else:
        default_updates = {}
    result = []
    all_keys = set(dict_values.keys()).union(dict_updates.keys())
    for value_key in all_keys:
        value = dict_values.get(value_key, {})
        specific_update = dict_updates.get(value_key, {})
        merged = merge_dict(
            original=value,
            updates=merge_dict(original=default_updates, updates=specific_update),
            merge_functions=merge_functions,
            key_order=object_key_order,
        )
        merged[key] = value_key
        result.append(merged)
    return sort_list_of_dicts_by_key(result, key=key)
