from fuso.factory import create_merge_factory


def test_merge_factory():
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
    factory = create_merge_factory(merge_functions={"b": merge_lists})
    assert (
        factory(
            original,
            updates,
        )
        == expected_output
    )
