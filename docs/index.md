---
title: Fuso
description: A customizable library for deeply merging dictionaries in Python.
keywords: dictionary merge, deep merge, python library, fuso, fusione
layout: docs
---

<p align="center">
  <img src="assets/logo.png" width="350" title="fuso logo">
</p>

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://pypi.org/project/fuso/)
[![PyPI Version](https://badge.fury.io/py/fuso.svg)](https://pypi.org/project/fuso/)
[![Read the Docs](https://app.readthedocs.org/projects/fuso/badge/?version=latest)](https://fuso.readthedocs.io/)

`fuso` comes from the Italian word _fusione_, which translates to _fusion_. This is exactly what this library does; it creates a fusion between two dictionaries.

The goal of this library is to offer a customizable way of deeply merging dictionaries. In its simplest form, `fuso` offers an experience like other well-established dictionary merging libraries such as [`deepmerge`](https://pypi.org/project/deepmerge/), [`mergedeep`](https://pypi.org/project/mergedeep/).

However, where this library differs is that it allows the user to specify custom `merge_functions` that should be applied for specific dot paths.

For example, you may want to concatenate lists found at the dot path `settings.plugins`, but for other lists, you may want to replace them entirely. With `fuso`, this is possible.
