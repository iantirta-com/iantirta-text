# Installation

## Basic Installation

Install the package from PyPI:

```bash
pip install iantirta-text
```

The core package has no required third-party runtime dependencies.

## Chinese Romanization

Chinese romanization requires `pypinyin`:

```bash
pip install "iantirta-text[zh]"
```

Then:

```python
from iantirta.text import romanize

print(romanize("你好"))
```

## Japanese Romanization

Japanese romanization requires `pykakasi`:

```bash
pip install "iantirta-text[ja]"
```

Then:

```python
from iantirta.text import romanize

print(romanize("日本語です"))
```

## Chinese and Japanese

To install both:

```bash
pip install "iantirta-text[romanize]"
```

