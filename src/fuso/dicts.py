from collections.abc import Callable
from typing import Any

from fuso.utils import sort_dict


def merge_dict(
    original: dict | None,
    updates: dict | None,
    merge_functions: dict[str, Callable[[Any, Any], Any]] | None = None,
    post_processor: Callable[[dict], dict] | None = None,
    key_order: list[str] | None = None,
) -> dict:
    """Merge two dictionaries.

    Args:
        original (dict): Original dictionary
        updates (dict): Dictionary with updates
        merge_functions (dict[str, Callable[[Any, Any], Any]] | None):
            Dictionary of functions to use for merging specific keys
        post_processor (callable | None): Function to process the result after merging
        key_order (list[str] | None): Non-exhaustive list of keys to sort by

    Returns:
        dict: Merged dictionary

    Example:
        ```py
        original = {
            "name": "Alice",
            "age": 30,
            "tags": ["user"],
        }
        updates = {
            "age": 31,
            "tags": ["editor"],
        }
        merged = merge_dict(
            original,
            updates,
            merge_functions={
                "age": lambda o, u: min(o, u),
            },
            post_processor=lambda d: d.update({"name": d["name"].upper()})
        )
        assert merged == {
            "name": "ALICE",
            "age": 30,
            "tags": ["user", "editor"],
        }
        ```
    """
    if merge_functions is None:
        merge_functions = {}
    original = original or {}
    updates = updates or {}
    result = {}
    all_keys = set(original.keys()).union(updates.keys())
    for key in all_keys:
        original_value = original.get(key)
        update_value = updates.get(key)
        merge_function = merge_functions.get(key)
        if merge_function:
            result[key] = merge_function(original_value, update_value)
        elif update_value is None:
            result[key] = original_value
        else:
            result[key] = _merge(original_value, update_value)
    if post_processor:
        result = post_processor(result)
    return sort_dict(result, key_order=key_order)


def _merge(
    value: list | dict | str | int | float | None,
    update: list | dict | str | int | float | None,
) -> list | dict | str | int | float | None:
    if value is not None and update is not None and type(value) is not type(update):
        raise TypeError(
            f"Cannot merge different types: {type(value)} and {type(update)}"
        )
    if value is None:
        return update
    elif update is None:
        return value
    elif isinstance(value, list) and isinstance(update, list):
        return value + update
    elif isinstance(value, dict) and isinstance(update, dict):
        result = {}
        all_keys = set(value.keys()).union(update.keys())
        for key in all_keys:
            result[key] = _merge(value.get(key), update.get(key))
        return result
    return update
