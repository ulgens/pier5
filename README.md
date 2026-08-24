<div align="center">

# pier5

[![Python](https://img.shields.io/badge/python->=3.12,<3.16-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![uv](https://img.shields.io/badge/-uv-DE5FE9?logo=uv&labelColor=555)](https://github.com/astral-sh/uv)
[![prek](https://img.shields.io/badge/-prek-F54327?logo=prek&labelColor=555)](https://github.com/j178/prek)
[![Ruff](https://img.shields.io/badge/-ruff-D7FF64?logo=ruff&labelColor=555)](https://github.com/astral-sh/ruff)
[![ty](https://img.shields.io/badge/-ty-46EBE1?logo=ty&labelColor=555)](https://github.com/astral-sh/ty)
[![Renovate](https://img.shields.io/badge/-renovate-308BE3?logo=renovate&labelColor=555)](https://github.com/renovatebot/renovate)

[![Git Hooks](https://img.shields.io/github/actions/workflow/status/ulgens/pier5/git-hooks.yml?logo=github&label=Git%20Hooks)](https://github.com/ulgens/pier5/actions/workflows/git-hooks.yml)
[![Tests](https://img.shields.io/github/actions/workflow/status/ulgens/pier5/tests.yml?logo=github&label=Tests)](https://github.com/ulgens/pier5/actions/workflows/tests.yml)

</div>

More Pythonic take on Processing Python interface

## Installation

```bash
pip install pier5
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv pip install pier5
```

## Usage

```python
from pier5 import __version__

print(__version__)
```

## Contribution
- Install git hooks with `prek install` and ensure your changes pass the checks before creating a pull request.
  - After `prek install`, git hooks will be automatically run while committing. To manually run the checks, use `prek run`.

## Updating the project template

This project was generated from a [Copier](https://copier.readthedocs.io/) template. To pull in the latest changes from the template:

```bash
copier update --trust
```

Resolve any conflicts if prompted. See the [python-anything](https://github.com/ulgens/python-anything) repository for template changelog and details.
