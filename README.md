# iantirta-text

[![PyPI](https://img.shields.io/pypi/v/iantirta-text.svg)](https://pypi.org/project/iantirta-text/)
[![Python](https://img.shields.io/pypi/pyversions/iantirta-text.svg)](https://pypi.org/project/iantirta-text/)
[![Tests](https://github.com/iantirta-com/iantirta-text/actions/workflows/test.yml/badge.svg)](https://github.com/iantirta-com/iantirta-text/actions/workflows/test.yml)
[![License](https://img.shields.io/github/license/iantirta-com/iantirta-text.svg)](https://github.com/iantirta-com/iantirta-text/blob/main/LICENSE)

[![Documentation](https://img.shields.io/badge/docs-online-blue.svg)](https://iantirta-com.github.io/iantirta-text/)
[![GitHub](https://img.shields.io/badge/GitHub-iantirta--com-181717?logo=github)](https://github.com/iantirta-com/iantirta-text)

Text processing and sequence utilities for Python.

`iantirta-text` provides small, composable utilities for working with
Unicode text, normalization, romanization, and filtering.


## Installation

```bash
pip install iantirta-text
```

Optional language support:

```bash
pip install "iantirta-text[zh]"
pip install "iantirta-text[ja]"
pip install "iantirta-text[romanize]"
```

## Quick Start

```python
from iantirta.text import normalize, romanize, filter_text

text = normalize("  Hello, 世界!  ")

print(text)
```

Romanization:

```python
from iantirta.text import romanize

print(romanize("你好"))
# ni hao

print(romanize("日本語です"))
# nihongo desu

print(romanize("hello 你好 日本語です"))
# hello ni hao nihongo desu
```

Filtering:

```python
from iantirta.text import filter_text

print(filter_text(
    "hello world",
    ["world"],
))

# hello
```

## Documentation

See the [full documentation](https://iantirta-com.github.io/iantirta-text/).

## Project

- [Repository](https://github.com/iantirta-com/iantirta-text)
- [PyPI](https://pypi.org/project/iantirta-text/)
- [Documentation](https://iantirta-com.github.io/iantirta-text/)
- License: Apache-2.0

