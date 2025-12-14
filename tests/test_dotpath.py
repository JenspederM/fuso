import pytest

from fuso.dotpath import from_dotpath, to_dotpath


@pytest.mark.parametrize(
    "value,expected",
    [
        (123, 123),
        (False, False),
        (None, None),
        (["a.b.c", {"a.b": 1, "a.c": 2}], ["a.b.c", {"a": {"b": 1, "c": 2}}]),
        ("a.b.c", "a.b.c"),
        ({"a.b": 1, "a.c": 2}, {"a": {"b": 1, "c": 2}}),
        ({"a.b.c": [1, 2, 3]}, {"a": {"b": {"c": [1, 2, 3]}}}),
        ({"a.b": {"c.d": 4, "e": 5}}, {"a": {"b": {"c": {"d": 4}, "e": 5}}}),
        ([None], [None]),
    ],
)
def test_from_dotpath(value, expected):
    assert from_dotpath(value) == expected


def test_from_dotpath_with_ignores():
    value = {
        "a.b.c": 1,
        "a.b.d": 2,
        "x.y": 3,
        "ignore.this.key": 4,
    }
    expected = {
        "a": {
            "b": {
                "c": 1,
                "d": 2,
            }
        },
        "x": {
            "y": 3,
        },
        "ignore.this.key": 4,
    }
    result = from_dotpath(value, dotpath_ignores=["ignore.this.key"])
    assert result == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (
            {"a": {"b": {"c": 1, "d": 2}}, "x": {"y": 3}},
            {"a.b.c": 1, "a.b.d": 2, "x.y": 3},
        ),
        (
            {"key": "value", "nested": {"inner.key": "inner.value"}},
            {"key": "value", "nested.inner.key": "inner.value"},
        ),
        (
            {"list": [{"a": 1}, {"b": 2}], "values": [10, 20]},
            {"list": [{"a": 1}, {"b": 2}], "values": [10, 20]},
        ),
        ({"simple": "test"}, {"simple": "test"}),
        ({"a": {"b": {"c": {"d": {"e": [123, 123]}}}}}, {"a.b.c.d.e": [123, 123]}),
    ],
)
def test_to_dotpath(value, expected):
    result = to_dotpath(value)
    assert result == expected
