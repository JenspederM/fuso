from fuso.merge import merge_dict


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
