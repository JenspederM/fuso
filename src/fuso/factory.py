from collections.abc import Callable

from fuso.merge import merge


def create_merge_factory(
    merge_functions: dict[str, Callable[[object, object], object]] | None = None,
    key_order: list[str] | None = None,
    post_processor: Callable[[dict], dict] | None = None,
) -> Callable[[dict, dict], dict]:
    """Create a merge function that merges dictionaries of dictionaries.

    Args:
        merge_functions (dict[str, Callable[[object, object], object]] | None):
            Dictionary of functions to use for merging specific keys
        key_order (list[str] | None): List of keys to determine the order of merging.

    Returns:
        Callable: Function that merges two dictionaries of dictionaries
    """

    def factory(values, updates):
        return merge(
            values,
            updates,
            merge_functions=merge_functions,
            key_order=key_order,
            post_processor=post_processor,
        )

    return factory
