import pytest

from fuso.merge import merge


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
            {"a": 1, "b": [1, 2, 3, 4], "c": 4},
        ),
        (
            {"a": {"x": 1}, "b": 2},
            {"a": {"y": 2}, "b": 3},
            {"a": {"x": 1, "y": 2}, "b": 3},
        ),
        (
            {"a": {"x": 1, "y": [1, 2]}, "b": 2},
            {"a": {"y": [3, 4]}, "b": 3},
            {"a": {"x": 1, "y": [1, 2, 3, 4]}, "b": 3},
        ),
        (
            {"a": {"x": 1, "y": [1, 2]}, "b": 2},
            {"a": {"y": None}, "b": 3},
            {"a": {"x": 1, "y": [1, 2]}, "b": 3},
        ),
        (
            {"a": {"x": 1, "y": None}, "b": 2},
            {"a": {"y": [1, 2]}, "b": 3},
            {"a": {"x": 1, "y": [1, 2]}, "b": 3},
        ),
        (
            {"a": {"x": {"z": 1}, "y": None}, "b": 2},
            {"a": {"x": {"w": 2}}, "b": 3},
            {"a": {"x": {"z": 1, "w": 2}, "y": None}, "b": 3},
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


def test_merge_with_key_order():
    original = {
        "b": 2,
        "a": 1,
        "c": 3,
    }
    updates = {
        "c": 4,
        "a": 5,
    }
    expected_output = {
        "a": 5,
        "b": 2,
        "c": 4,
    }
    result = merge(original, updates, key_order=["a", "b", "c"])
    assert result == expected_output
    assert list(result.keys()) == ["a", "b", "c"]


def test_merge_with_key_order_partial():
    original = {
        "b": 2,
        "a": 1,
        "c": 3,
    }
    updates = {
        "c": 4,
        "a": 5,
    }
    expected_output = {
        "a": 5,
        "b": 2,
        "c": 4,
    }
    result = merge(original, updates, key_order=["a", "c"])
    assert result == expected_output
    assert list(result.keys()) == ["a", "c", "b"]


def test_merge_with_key_order_none():
    original = {
        "b": 2,
        "a": 1,
        "c": 3,
    }
    updates = {
        "c": 4,
        "a": 5,
    }
    expected_output = {
        "a": 5,
        "b": 2,
        "c": 4,
    }
    result = merge(original, updates, key_order=None)
    assert result == expected_output
    # Order may vary since no key_order is provided
    assert set(result.keys()) == {"a", "b", "c"}


def test_merge_type_mismatch():
    original = {
        "a": 1,
    }
    updates = {
        "a": [2, 3],
    }
    with pytest.raises(
        TypeError,
        match="Cannot merge different types: <class 'int'> and <class 'list'>",
    ):
        merge(original, updates)
