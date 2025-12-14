import pytest

from fuso.merge import merge, merge_dict, merge_list_of_dicts_by_key


@pytest.mark.parametrize(
    "values,updates,key,expected_output",
    [
        (
            [
                {"id": 1, "name": "Alice", "age": 30},
                {"id": 2, "name": "Bob", "age": 25},
            ],
            [
                {"id": 1, "age": 31},
                {"id": 3, "name": "Charlie", "age": 20},
            ],
            "id",
            [
                {"id": 1, "name": "Alice", "age": 31},
                {"id": 2, "name": "Bob", "age": 25},
                {"id": 3, "name": "Charlie", "age": 20},
            ],
        ),
    ],
)
def test_merge_list_of_dicts_by_key(values, updates, key, expected_output):
    assert merge_list_of_dicts_by_key(values, updates, key=key) == expected_output


def test_merge_list_of_dicts_by_key_empty():
    values = []
    updates = []
    expected_output = []
    assert merge_list_of_dicts_by_key(values, updates, key="id") == expected_output


def test_merge_list_of_dicts_by_key_no_overlap():
    values = [
        {"id": 1, "name": "Alice", "age": 30},
    ]
    updates = [
        {"id": 2, "name": "Bob", "age": 25},
    ]
    expected_output = [
        {"id": 1, "name": "Alice", "age": 30},
        {"id": 2, "name": "Bob", "age": 25},
    ]
    assert merge_list_of_dicts_by_key(values, updates, key="id") == expected_output


def test_merge_list_of_dicts_by_key_all_overlap():
    values = [
        {"id": 1, "name": "Alice", "age": 30},
    ]
    updates = [
        {"id": 1, "age": 31},
    ]
    expected_output = [
        {"id": 1, "name": "Alice", "age": 31},
    ]
    assert merge_list_of_dicts_by_key(values, updates, key="id") == expected_output


def test_merge_list_of_dicts_by_key_keyerror_value():
    values = [
        {"uid": 1, "name": "Alice", "age": 30},
    ]
    updates = [
        {"id": 1, "age": 31},
    ]
    with pytest.raises(
        KeyError, match="Key 'id' not found in value. Available keys: uid, name, age"
    ):
        merge_list_of_dicts_by_key(values, updates, key="id")


def test_merge_list_of_dicts_by_key_keyerror_update():
    values = [
        {"id": 1, "name": "Alice", "age": 30},
    ]
    updates = [
        {"uid": 1, "age": 31},
    ]
    with pytest.raises(
        KeyError, match="Key 'id' not found in update. Available keys: uid, age"
    ):
        merge_list_of_dicts_by_key(values, updates, key="id")


def test_merge_list_of_dicts_by_key_with_default():
    values = [
        {"id": 1, "name": "Alice", "age": 30},
        {"id": 2, "name": "Bob", "age": 25},
    ]
    updates = [
        {"id": "default", "age": 35},
        {"id": 2, "name": "Robert"},
    ]
    expected_output = [
        {"id": 1, "name": "Alice", "age": 35},
        {"id": 2, "name": "Robert", "age": 35},
    ]
    assert (
        merge_list_of_dicts_by_key(values, updates, key="id", default_key="default")
        == expected_output
    )


def test_merge_list_of_dicts_by_key_with_merge_functions():
    def merge_ages(age1, age2):
        return max(age1, age2)

    values = [
        {"id": 1, "name": "Alice", "age": 30},
        {"id": 2, "name": "Bob", "age": 25},
    ]
    updates = [
        {"id": 1, "age": 35},
        {"id": 2, "age": 20},
    ]
    expected_output = [
        {"id": 1, "name": "Alice", "age": 35},
        {"id": 2, "name": "Bob", "age": 25},
    ]
    assert (
        merge_list_of_dicts_by_key(
            values,
            updates,
            key="id",
            merge_functions={"age": merge_ages},
        )
        == expected_output
    )


def test_merge_list_of_dicts_by_key_empty_updates():
    values = [
        {"id": 1, "name": "Alice", "age": 30},
        {"id": 2, "name": "Bob", "age": 25},
    ]
    updates = []
    expected_output = [
        {"id": 1, "name": "Alice", "age": 30},
        {"id": 2, "name": "Bob", "age": 25},
    ]
    assert merge_list_of_dicts_by_key(values, updates, key="id") == expected_output


def test_merge_list_of_dicts_by_key_empty_values():
    values = []
    updates = [
        {"id": 1, "name": "Alice", "age": 30},
        {"id": 2, "name": "Bob", "age": 25},
    ]
    expected_output = [
        {"id": 1, "name": "Alice", "age": 30},
        {"id": 2, "name": "Bob", "age": 25},
    ]
    assert merge_list_of_dicts_by_key(values, updates, key="id") == expected_output


def test_merge_dict_empty_updates():
    values = {"a": 1, "b": 2}
    updates = {}
    expected_output = {"a": 1, "b": 2}
    assert merge_dict(values, updates) == expected_output


def test_merge_dict_empty_values():
    values = {}
    updates = {"a": 3, "b": 4}
    expected_output = {"a": 3, "b": 4}
    assert merge_dict(values, updates) == expected_output


def test_merge_dict_with_merge_functions():
    def merge_values(val1, val2):
        return val1 + val2

    values = {"a": 1, "b": 2}
    updates = {"a": 3, "b": 4}
    expected_output = {"a": 4, "b": 6}
    assert (
        merge_dict(
            values,
            updates,
            merge_functions={"a": merge_values, "b": merge_values},
        )
        == expected_output
    )


def test_merge_dict_no_overlap():
    values = {"a": 1, "b": 2}
    updates = {"c": 3, "d": 4}
    expected_output = {"a": 1, "b": 2, "c": 3, "d": 4}
    assert merge_dict(values, updates) == expected_output


def test_merge_dict_all_overlap():
    values = {"a": 1, "b": 2}
    updates = {"a": 3, "b": 4}
    expected_output = {"a": 3, "b": 4}
    assert merge_dict(values, updates) == expected_output


def test_merge_dict_partial_overlap():
    values = {"a": 1, "b": 2}
    updates = {"b": 3, "c": 4}
    expected_output = {"a": 1, "b": 3, "c": 4}
    assert merge_dict(values, updates) == expected_output


def test_merge_dict_key_order():
    values = {"b": 2, "a": 1, "c": 3}
    updates = {"c": 4, "a": 5}
    expected_output = {"a": 5, "b": 2, "c": 4}
    result = merge_dict(values, updates, key_order=["a", "b", "c"])
    assert result == expected_output
    assert list(result.keys()) == ["a", "b", "c"]


def test_merge_dict_key_order_partial():
    values = {"b": 2, "a": 1, "c": 3}
    updates = {"c": 4, "a": 5}
    expected_output = {"a": 5, "b": 2, "c": 4}
    result = merge_dict(values, updates, key_order=["a", "c"])
    assert result == expected_output
    assert list(result.keys()) == ["a", "c", "b"]


def test_merge_dict_key_order_none():
    values = {"b": 2, "a": 1, "c": 3}
    updates = {"c": 4, "a": 5}
    expected_output = {"a": 5, "b": 2, "c": 4}
    result = merge_dict(values, updates, key_order=None)
    assert result == expected_output
    # Order may vary since no key_order is provided
    assert set(result.keys()) == {"a", "b", "c"}


@pytest.mark.parametrize(
    "original,updates,expected_output",
    [
        (
            {"a": 1, "b": 2},
            {"b": 3, "c": 4},
            {"a": 1, "b": 3, "c": 4},
        ),
        (
            {"a": {"x": 1, "y": 2}, "b": 2},
            {"a": {"y": 3, "z": 4}, "c": 4},
            {"a": {"x": 1, "y": 3, "z": 4}, "b": 2, "c": 4},
        ),
        (
            {"a": 1, "b": [1, 2]},
            {"b": [3, 4], "c": 4},
            {"a": 1, "b": [3, 4], "c": 4},
        ),
        (
            {"a": {"x": 1}, "b": 2},
            {"a": {"y": 2}, "b": 3},
            {"a": {"x": 1, "y": 2}, "b": 3},
        ),
        (
            {"a": {"x": 1, "y": [1, 2]}, "b": 2},
            {"a": {"y": [3, 4]}, "b": 3},
            {"a": {"x": 1, "y": [3, 4]}, "b": 3},
        ),
        (
            {"a": {"x": 1, "y": [1, 2]}, "b": 2},
            {"a": {"y": None}, "b": 3},
            {"a": {"x": 1, "y": [1, 2]}, "b": 3},
        ),
    ],
)
def test_merge(original, updates, expected_output):
    assert merge(original, updates) == expected_output


def test_merge_with_merge_functions():
    def merge_lists(l1, l2):
        return l1 + l2 if l1 and l2 else l1 or l2 or []

    original = {
        "a": {"x": 1, "y": 2},
        "b": [1, 2],
    }
    updates = {
        "a": {"y": 3, "z": 4},
        "b": [3, 4],
    }
    expected_output = {
        "a": {"x": 1, "y": 3, "z": 4},
        "b": [1, 2, 3, 4],
    }
    assert (
        merge(
            original,
            updates,
            merge_functions={"b": merge_lists},
        )
        == expected_output
    )


def test_merge_with_none_updates():
    original = {
        "a": 1,
        "b": 2,
    }
    updates = {
        "a": None,
        "b": 3,
    }
    expected_output = {
        "a": 1,
        "b": 3,
    }
    assert merge(original, updates) == expected_output


def test_merge_with_none_values():
    original = {
        "a": None,
        "b": 2,
    }
    updates = {
        "a": 1,
        "b": None,
    }
    expected_output = {
        "a": 1,
        "b": 2,
    }
    assert merge(original, updates) == expected_output


def test_merge_both_empty():
    original = {}
    updates = {}
    expected_output = {}
    assert merge(original, updates) == expected_output


def test_merge_with_postprocessor():
    def postprocessor(merged):
        if "total" in merged:
            merged["total"] += 10
        return merged

    original = {
        "a": 1,
        "total": 5,
    }
    updates = {
        "b": 2,
        "total": 15,
    }
    expected_output = {
        "a": 1,
        "b": 2,
        "total": 25,  # 15 from updates + 10 from postprocessor
    }
    assert merge(original, updates, post_processor=postprocessor) == expected_output
