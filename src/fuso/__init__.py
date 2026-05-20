"""Fuso is a Python library for merging and manipulating dictionaries and lists of
dictionaries.

Fuso provides functions for merging dictionaries and lists of dictionaries, sorting, and
converting between different data structures. It also includes a factory function for
creating custom merge functions.
"""

from fuso.dicts import merge_dict
from fuso.factories import (
    create_merge_factory,
    create_merge_list_of_dicts_by_key_factory,
)
from fuso.lists import merge_list_of_dicts_by_key
from fuso.utils import sort_dict, sort_list_of_dicts_by_key, to_list_of_dicts_by_key

__all__ = [
    "merge_dict",
    "merge_list_of_dicts_by_key",
    "to_list_of_dicts_by_key",
    "sort_dict",
    "sort_list_of_dicts_by_key",
    "create_merge_factory",
    "create_merge_list_of_dicts_by_key_factory",
]
