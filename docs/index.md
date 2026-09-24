# iantirta-text

Text processing and sequence utilities for Python.

`iantirta-text` provides small, composable utilities for working with
Unicode text, normalization, romanization, and filtering.

## Installation

```bash
pip install iantirta-text
```

## Quick Start

```python
from iantirta.text import normalize, romanize, filter_text

text = normalize("  Hello, 世界!  ")

print(text)
```

## Features

- Unicode-aware text normalization
- Text filtering
- Chinese romanization
- Japanese romanization
- Optional dependencies for language-specific processing

## Next Steps

- [Installation](installation.md)
- [Normalization](normalize.md)
- [Romanization](romanize.md)
- [Filtering](filter.md)
