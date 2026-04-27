"""Functions for merging dictionaries and lists of dictionaries.

Provides functions to merge two dictionaries or two lists of dictionaries
by a specified key, with support for custom merge functions and sorting.
"""

from collections.abc import Callable
from typing import Any

from fuso.utils import sort_dict, sort_list_of_dicts_by_key, to_list_of_dicts_by_key


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
            values=value,
            updates=merge_dict(values=default_updates, updates=specific_update),
            merge_functions=merge_functions,
            key_order=object_key_order,
        )
        merged[key] = value_key
        result.append(merged)
    return sort_list_of_dicts_by_key(result, key=key)


def merge_dict(
    values: dict,
    updates: dict,
    merge_functions: dict[str, Callable[[Any, Any], Any]] | None = None,
    key_order: list[str] | None = None,
) -> dict:
    """Merge two dictionaries.

    Args:
        values (dict): Original dictionary
        updates (dict): Dictionary with updates
        merge_functions (dict[str, Callable[[Any, Any], Any]] | None):
            Dictionary of functions to use for merging specific keys
        key_order (list[str] | None): Non-exhaustive list of keys to sort by

    Returns:
        dict: Merged dictionary

    Example:
        ```py
        values = {
            "name": "Alice",
            "age": 30,
            "tags": ["user"],
        }
        updates = {
            "age": 31,
            "tags": ["editor"],
        }
        merged = merge_dict(values, updates)
        assert merged == {
            "name": "Alice",
            "age": 31,
            "tags": ["user", "editor"],
        }
        ```
    """
    result = {}
    all_keys = set(values.keys()).union(updates.keys())
    for key in all_keys:
        value = values.get(key)
        update = updates.get(key)
        merge_function = merge_functions.get(key) if merge_functions else None
        if merge_function:
            result[key] = merge_function(value, update)
        else:
            result[key] = _merge(value, update)
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


def merge(
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
        merged = merge(
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


def create_merge_factory(
    merge_functions: dict[str, Callable[[Any, Any], Any]] | None = None,
    key_order: list[str] | None = None,
    post_processor: Callable[[dict], dict] | None = None,
) -> Callable[[dict, dict], dict]:
    """Create a merge function that merges arbitrarily nested dictionaries.

    Args:
        merge_functions (dict[str, Callable[[Any, Any], Any]] | None):
            Dictionary of functions to use for merging specific keys
        key_order (list[str] | None): List of keys to determine the order of merging.
        post_processor (callable | None): Function to process the result after merging

    Returns:
        Callable: Function that merges two arbitrarily nested dictionaries.
    """

    def factory(values, updates):
        return merge(
            values,
            updates,
            merge_functions=merge_functions,
            key_order=key_order,
            post_processor=post_processor,
        )

    return factory


def create_merge_list_of_dicts_by_key_factory(
    key: str,
    default_key: str | None = None,
    merge_functions: dict[str, Callable[[Any, Any], Any]] | None = None,
    object_key_order: list[str] | None = None,
):
    """Create a merge function that merges two lists of dictionaries by a specified key.

    Args:
        key (str): Key to use for merging
        default_key (str | None): Key to use for default updates
        merge_functions (dict[str, Callable[[Any, Any], Any]] | None):
            Dictionary of functions to use for merging specific keys
        object_key_order (list[str] | None): Non-exhaustive list of keys to sort objects
            by

    Returns:
        Callable: Function that merges two lists of dictionaries by a specified key.
    """

    def factory(values, updates):
        return merge_list_of_dicts_by_key(
            values=values,
            updates=updates,
            key=key,
            default_key=default_key,
            merge_functions=merge_functions,
            object_key_order=object_key_order,
        )

    return factory
