# User Guide

Fuso can be used to merge and manipulate dictionaries and lists of dictionaries in various ways. This user guide provides examples of how to use Fuso's functions for merging, sorting, and converting data structures.

## Merge Factory

Fuso provides a factory function for creating custom merge functions. This allows you to define your own merge strategies for specific keys in your dictionaries.

```python test_create_merge_factory_example
from fuso import create_merge_factory

def custom_merge(value1, value2):
    return value1 + value2

merge_func = create_merge_factory(merge_functions={'b': custom_merge})
dict1 = {'a': 1, 'b': 2}
dict2 = {'a': 3, 'b': 3, 'c': 4}
merged_dict = merge_func(dict1, dict2)
assert merged_dict == {'a': 3, 'b': 5, 'c': 4}
```

This can also be used to create merge functions for lists of dictionaries, allowing you to specify how to merge dictionaries based on a common key.

```python test_create_merge_list_of_dicts_by_key_factory_example
from fuso import create_merge_list_of_dicts_by_key_factory

merge_by_id = create_merge_list_of_dicts_by_key_factory(
    key="id",
    merge_functions={"name": lambda x, y: y.upper() if y else x.upper()},
)
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
    {"id": 1, "name": "ALICE", "tags": ["user", "editor"]},
    {"id": 2, "name": "BOB", "tags": ["admin"]},
    {"id": 3, "name": "CHARLIE", "tags": ["user"]},
]
```

This allows you to easily create custom merge functions that can be reused across your codebase, making it easier to maintain and update your merging logic as needed.

## Merging Dictionaries

To merge two dictionaries, you can use the `merge_dict` function. This function takes two dictionaries as input and returns a new dictionary that contains the merged key-value pairs.

```python test_merge_dict_example
from fuso import merge_dict

dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 3, 'c': 4}

merged_dict = merge_dict(dict1, dict2)
assert merged_dict == {'a': 1, 'b': 3, 'c': 4}
```

If you want more control over how the dictionaries are merged, you can specify a custom merge strategy.

```python test_merge_with_custom_strategy_example
from fuso import merge_dict

dict1 = {'a': 1, 'b': 2}
dict2 = {'a': 3, 'b': 3, 'c': 4}

def custom_merge(value1, value2):
    return value1 + value2

merged_dict = merge_dict(dict1, dict2, merge_functions={'b': custom_merge})
assert merged_dict == {'a': 3, 'b': 5, 'c': 4}
```

## Merging Lists of Dictionaries
To merge two lists of dictionaries based on a common key, you can use the `merge_list_of_dicts_by_key` function. This function takes two lists of dictionaries and a key to merge by, and returns a new list of dictionaries that contains the merged entries.

```python test_merge_list_of_dicts_by_key_example
from fuso import merge_list_of_dicts_by_key

list1 = [
    {'id': 1, 'name': 'Alice', 'tags': ['user']},
    {'id': 2, 'name': 'Bob', 'tags': ['admin']},
]
list2 = [
    {'id': 1, 'tags': ['editor']},
    {'id': 3, 'name': 'Charlie', 'tags': ['user']},
]

merged_list = merge_list_of_dicts_by_key(list1, list2, key='id')
assert merged_list == [
    {'id': 1, 'name': 'Alice', 'tags': ['user', 'editor']},
    {'id': 2, 'name': 'Bob', 'tags': ['admin']},
    {'id': 3, 'name': 'Charlie', 'tags': ['user']},
]
```