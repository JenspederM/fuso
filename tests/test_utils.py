import pytest

from fuso.utils import sort_dict, to_list_of_dicts_by_key


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
            {"two": 2, "one": 1, "three": 3},
            [],
            ["two", "one", "three"],
        ),
        (
            {"two": 2, "one": 1, "three": 3},
            ["three", "two", "one"],
            ["three", "two", "one"],
        ),
    ],
)
def test_sort_dict(value, key_order, expected_keys):
    sorted_dict = sort_dict(value, key_order)
    assert list(sorted_dict.keys()) == expected_keys
