# Fuso

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Download/Month](https://img.shields.io/pypi/dm/fuso)](https://pypi.org/project/fuso/)
[![PyPI Version](https://badge.fury.io/py/fuso.svg)](https://pypi.org/project/fuso/)
[![Read the Docs](https://app.readthedocs.org/projects/fuso/badge/?version=latest)](https://fuso.readthedocs.io/)

`fuso` comes from the Italian word _fusione_, which translates to _fusion_. This is exactly what this library does; it creates a fusion between two dictionaries.

The goal of this library is to offer a customizable way of deeply merging dictionaries. In its simplest form, `fuso` offers an experience like other well-established dictionary merging libraries such as [`deepmerge`](https://pypi.org/project/deepmerge/), [`mergedeep`](https://pypi.org/project/mergedeep/).

However, where this library differs is that it allows the user to specify custom `merge_functions` for specific keys.

For example, you may want to concatenate lists for one key, but keep overwrite behavior for other keys. With `fuso`, this is possible.

## Installation
You can install `fuso` via pip:

```bash
pip install fuso
```

## Usage
Here's a basic example of how to use `fuso` to merge two dictionaries:

```python
from fuso import merge_dict

dict1 = {
    "settings": {
        "theme": "dark",
        "plugins": ["plugin1", "plugin2"]
    }
}
dict2 = {
    "settings": {
        "plugins": ["plugin3"],
        "language": "en"
    }
}
merged_dict = merge_dict(dict1, dict2)
print(merged_dict)
# {
#    "settings": {
#      "theme": "dark",
#      "plugins": ["plugin1", "plugin2", "plugin3"],
#      "language": "en"
#    }
# }
```

### Merge semantics

- Dicts are merged recursively.
- Lists are concatenated.
- Scalars are overwritten by `updates`.
- `None` in `updates` keeps the original value.
- Merging non-`None` values of different types raises `TypeError`.
- Duplicate lookup keys in `to_list_of_dicts_by_key` raise `KeyError`.

### Ordering

- `merge_dict` returns keys sorted alphabetically by default.
- You can control key order with `key_order` (partial orders are supported).

## Documentation
For more detailed documentation, including advanced usage and customization options, please visit the [official documentation](https://fuso.readthedocs.io).

## Contributing
Contributions are welcome! Please feel free to submit issues or pull requests on the [GitHub repository](https://github.com/jenspederm/fuso).

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Changes

To see changes by version check the [changelog](docs/changelog.md).
