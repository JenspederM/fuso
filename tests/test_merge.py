import pytest

from fuso.merge import merge_list_of_dicts_by_key


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
