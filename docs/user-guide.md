# User Guide

Fuso helps you merge structured data while keeping merge behavior explicit and predictable.
This guide explains what each API is for, how the merge rules work, and where to apply
each function in real projects.

If you are new to the library, read from top to bottom once. After that, this page can be
used as a reference when choosing between direct merge calls, factory functions, and list
merging with defaults.

## Merge Factory

Factory functions are useful when you want to define a merge policy once and reuse it in
multiple places. Instead of passing merge options every time, you create a callable with
your preferred configuration.

The example below creates a reusable dictionary merge function with a custom strategy for
one key.

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

The same pattern exists for lists of dictionaries. You choose a key used to identify items,
and the resulting factory merges list items by that key whenever you call it.

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

Use factories when merge behavior should be shared by multiple modules, jobs, or endpoints.
It keeps merge configuration centralized and reduces repeated argument wiring.

## Merging Dictionaries

Use `merge_dict` when working with nested configuration-like data where updates should be
applied deeply, not only at the top level. The function returns a new merged dictionary
based on the original values and incoming updates.

```python test_merge_dict_example
from fuso import merge_dict

dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 3, 'c': 4}

merged_dict = merge_dict(dict1, dict2)
assert merged_dict == {'a': 1, 'b': 3, 'c': 4}
```

When a specific key needs custom behavior, pass a function in `merge_functions`. This lets
you override the default rule for that key while keeping default behavior for all others.

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
Use `merge_list_of_dicts_by_key` when your data is a collection of objects and each object
has an identity key such as `id` or `name`. Fuso converts each list into an internal lookup,
merges objects with matching keys, and returns a merged list.

The merge key must be unique within each input list. Duplicate keys are rejected with a
`KeyError` so ambiguous merges fail early.

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

## Merge Semantics

`merge_dict` applies a small set of deterministic rules. Knowing these rules makes merge
results easy to reason about:

- Dictionary values are merged recursively, key by key.
- List values are concatenated in order: original items first, update items after.
- Scalar values are replaced by the update value.
- `None` in `updates` means keep the original value.
- Different non-`None` value types raise `TypeError`.

```python test_merge_semantics_none_and_type_example
from fuso import merge_dict

original = {
    "a": {"x": 1, "tags": ["user"]},
    "b": 10,
}
updates = {
    "a": {"tags": ["editor"]},
    "b": None,
}

merged = merge_dict(original, updates)
assert merged == {
    "a": {"x": 1, "tags": ["user", "editor"]},
    "b": 10,
}
```

## Ordering

Fuso aims to return stable, predictable output ordering.

`merge_dict` sorts keys alphabetically by default. If you need a presentation-specific
order, pass `key_order`.

```python test_merge_dict_key_order_example
from fuso import merge_dict

original = {"b": 2, "a": 1, "c": 3}
updates = {"a": 5, "d": 4}

merged = merge_dict(original, updates, key_order=["d", "a"])
assert list(merged.keys()) == ["d", "a", "b", "c"]
assert merged == {"d": 4, "a": 5, "b": 2, "c": 3}
```

`merge_list_of_dicts_by_key` returns items sorted by the merge key, which keeps output
stable regardless of input list order.

```python test_merge_list_sorted_by_key_example
from fuso import merge_list_of_dicts_by_key

values = [{"id": 2, "name": "Bob"}]
updates = [{"id": 1, "name": "Alice"}]

merged = merge_list_of_dicts_by_key(values, updates, key="id")
assert [item["id"] for item in merged] == [1, 2]
```

## Defaults for List Merging

`default_key` lets you define shared updates once and apply them to all list items.
Per-item updates are then applied on top of those defaults.

In other words, the precedence is:

1. Existing item value
2. Default update (from `default_key`)
3. Item-specific update

```python test_merge_list_default_key_example
from fuso import merge_list_of_dicts_by_key

values = [
    {"id": 1, "name": "Alice", "age": 30},
    {"id": 2, "name": "Bob", "age": 25},
]
updates = [
    {"id": "default", "age": 35},
    {"id": 2, "name": "Robert"},
]

merged = merge_list_of_dicts_by_key(values, updates, key="id", default_key="default")
assert merged == [
    {"id": 1, "name": "Alice", "age": 35},
    {"id": 2, "name": "Robert", "age": 35},
]
```

## Building Override Pipelines

One of the most useful ways to use Fuso is not as a one-off merge helper, but as the core
of an override pipeline.

In that style, you first define a merge policy for your domain. Then you apply multiple
layers of configuration in a deliberate order. This works well for cases such as:

- base configuration plus environment-specific overrides
- shared defaults plus per-resource overrides
- reusable application settings plus customer-specific adjustments

The key idea is that Fuso lets you separate two concerns:

1. What counts as the same object and how matching objects should be merged
2. In what order different override layers should be applied

The example below defines a reusable overrider for an application config. Services are
merged by `name`, while top-level keys follow the normal dictionary merge rules.

```python test_building_override_pipeline_example
from fuso import create_merge_factory, merge_list_of_dicts_by_key

config_overrider = create_merge_factory(
    merge_functions={
        "services": lambda old, new: merge_list_of_dicts_by_key(
            old or [], new or [], key="name"
        )
    },
    key_order=["name", "region", "services", "tags"],
)

base_config = {
    "name": "analytics",
    "services": [
        {"name": "api", "replicas": 2, "tags": ["public"]},
        {"name": "worker", "replicas": 1, "tags": ["batch"]},
    ],
    "tags": ["base"],
}

default_overrides = {
    "region": "eu-west-1",
    "services": [
        {"name": "api", "tags": ["monitored"]},
        {"name": "worker", "replicas": 2},
    ],
}

environment_overrides = {
    "services": [
        {"name": "api", "replicas": 3},
        {"name": "scheduler", "replicas": 1, "tags": ["cron"]},
    ],
    "tags": ["staging"],
}

merged = config_overrider(base_config, default_overrides)
merged = config_overrider(merged, environment_overrides)

assert merged == {
    "name": "analytics",
    "region": "eu-west-1",
    "services": [
        {"replicas": 3, "tags": ["public", "monitored"], "name": "api"},
        {"replicas": 1, "tags": ["cron"], "name": "scheduler"},
        {"replicas": 2, "tags": ["batch"], "name": "worker"},
    ],
    "tags": ["base", "staging"],
}
```

This pattern scales well because the merge policy stays in one place. Once you define the
overrider, the rest of your code can focus on selecting the right layers to apply.

When using Fuso this way, a good design approach is:

1. Start by identifying which lists represent collections of named objects.
2. Decide which key uniquely identifies each object in those collections.
3. Write custom merge functions only for fields that need domain-specific behavior.
4. Apply override layers in explicit precedence order, from least specific to most specific.

That is often the point where `create_merge_factory` becomes more valuable than calling
`merge_dict` directly at every call site.

## Errors and Edge Cases

Fuso validates merge inputs and raises clear errors when it cannot produce an unambiguous
result.

- If a required merge key is missing, `KeyError` includes the available keys from the
    offending object.
- `original` and `updates` may be `None` in `merge_dict`; they are treated as empty
    dictionaries.
- If `to_list_of_dicts_by_key` encounters duplicate lookup keys, it raises `KeyError`.

```python test_to_list_duplicate_keys_error_example
from fuso import to_list_of_dicts_by_key

values = [
    {"id": 1, "name": "Alice"},
    {"id": 1, "name": "Alicia"},
]

try:
    to_list_of_dicts_by_key(values, key="id")
    assert False, "Expected a KeyError for duplicate keys"
except KeyError as error:
    assert str(error) == '"Duplicate key \'1\' found for lookup key \'id\'"'
```

## Cookbook

### Keep Maximum Numeric Value

```python test_cookbook_keep_max_example
from fuso import merge_dict

def keep_max(old, new):
    if old is None:
        return new
    if new is None:
        return old
    return max(old, new)

merged = merge_dict(
    {"name": "Alice", "age": 30},
    {"age": 25},
    merge_functions={"age": keep_max},
)
assert merged == {"age": 30, "name": "Alice"}
```

### Replace One List Key, Concatenate Another

```python test_cookbook_replace_vs_concat_lists_example
from fuso import merge_dict

merged = merge_dict(
    {
        "plugins": ["base"],
        "enabled_flags": ["a"],
    },
    {
        "plugins": ["custom"],
        "enabled_flags": ["b"],
    },
    merge_functions={"enabled_flags": lambda old, new: new or old or []},
)

assert merged == {
    "enabled_flags": ["b"],
    "plugins": ["base", "custom"],
}
```