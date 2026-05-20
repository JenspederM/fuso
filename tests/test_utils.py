import pytest

from fuso.utils import sort_dict, sort_list_of_dicts_by_key, to_list_of_dicts_by_key


def test_list_to_dict_by_key():
    input_data = [
        {"name": "item1", "value": 10},
        {"name": "item2", "value": 20},
    ]
    expected_output = {
        "item1": {"value": 10},
        "item2": {"value": 20},
    }
    assert to_list_of_dicts_by_key(input_data) == expected_output

    # Test with a different key
    input_data = [
        {"id": "item1", "value": 10},
        {"id": "item2", "value": 20},
    ]
    expected_output = {
        "item1": {"value": 10},
        "item2": {"value": 20},
    }
    assert to_list_of_dicts_by_key(input_data, key="id") == expected_output

    # Test KeyError
    input_data = [
        {"name": "item1", "value": 10},
        {"value": 20},
    ]
    with pytest.raises(
        KeyError, match="Key 'name' not found in value. Available keys: value"
    ):
        to_list_of_dicts_by_key(input_data)


def test_list_to_dict_by_key_empty():
    input_data = []
    expected_output = {}
    assert to_list_of_dicts_by_key(input_data) == expected_output


def test_list_to_dict_by_key_duplicate_key():
    input_data = [
        {"id": 1, "name": "Alice"},
        {"id": 1, "name": "Alicia"},
    ]
    with pytest.raises(KeyError, match="Duplicate key '1' found for lookup key 'id'"):
        to_list_of_dicts_by_key(input_data, key="id")


@pytest.mark.parametrize(
    "value,key_order,expected_keys",
    [
        (
            {"b": 2, "a": 1, "c": 3},
            ["a", "b"],
            ["a", "b", "c"],
        ),
        (
            {"x": 24, "y": 25, "z": 26},
            ["z", "x"],
            ["z", "x", "y"],
        ),
        (
            {"b": 2, "a": 1, "c": 3},
            [],
            ["a", "b", "c"],
        ),
        (
            {"b": 2, "a": 1, "c": 3},
            None,
            ["a", "b", "c"],
        ),
        (
            {"b": 2, "a": 1, "c": 3},
            ["c", "b", "a"],
            ["c", "b", "a"],
        ),
    ],
)
def test_sort_dict(value, key_order, expected_keys):
    sorted_dict = sort_dict(value, key_order)
    keys = list(sorted_dict.keys())
    for i in range(len(expected_keys)):
        assert keys[i] == expected_keys[i]


def test_sort_list_of_dicts_by_key():
    input_list = [
        {"name": "b", "value": 2},
        {"name": "a", "value": 1},
        {"name": "c", "value": 3},
    ]
    sorted_list = sort_list_of_dicts_by_key(input_list, key="name")
    assert [item["name"] for item in sorted_list] == ["a", "b", "c"]
