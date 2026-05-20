from collections.abc import Callable
from typing import Any

from fuso.dicts import merge_dict
from fuso.lists import merge_list_of_dicts_by_key


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

    Example:
        ```py
        merge_with_custom_functions = create_merge_factory(
            merge_functions={
                "age": lambda o, u: min(o, u),
            },
            post_processor=lambda d: d.update({"name": d["name"].upper()})
        )
        original = {
            "name": "Alice",
            "age": 30,
            "tags": ["user"],
        }
        updates = {
            "age": 31,
            "tags": ["editor"],
        }
        merged = merge_with_custom_functions(original, updates)
        assert merged == {
            "name": "ALICE",
            "age": 30,
            "tags": ["user", "editor"],
        }
        ```
    """

    def factory(values, updates):
        return merge_dict(
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
) -> Callable[[list[dict], list[dict]], list[dict]]:
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

    Example:
        ```py
        merge_by_id = create_merge_list_of_dicts_by_key_factory(key="id")
        values = [
            {"id": 1, "name": "Alice", "tags": ["user"]},
            {"id": 2, "name": "Bob", "tags": ["admin"]},
        ]
        updates = [
            {"id": 1, "tags": ["editor"]},
            {"id": 3, "name": "Charlie", "tags": ["user"]},
        ]
        merged = merge_by_id(values, updates)
        assert merged == [
            {"id": 1, "name": "Alice", "tags": ["user", "editor"]},
            {"id": 2, "name": "Bob", "tags": ["admin"]},
            {"id": 3, "name": "Charlie", "tags": ["user"]},
        ]
        ```
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
