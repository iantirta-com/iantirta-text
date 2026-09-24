# iantirta-text

Text processing and sequence utilities for Python.

`iantirta-text` provides small, composable utilities for working with
Unicode text, normalization, romanization, filtering, and eventually
sequence and phonetic processing.

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

See the full documentation:

https://iantirta-com.github.io/iantirta-text/

## Project

- Repository: https://github.com/iantirta-com/iantirta-text⁠
- PyPI: https://pypi.org/project/iantirta-text/⁠
- License: Apache-2.0

