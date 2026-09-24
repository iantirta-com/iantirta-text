# Romanization

The `romanize()` function converts supported non-Latin scripts into
Latin-script romanization while preserving existing Latin text.

## Chinese

Install Chinese support:

```bash
pip install "iantirta-text[zh]"
```

Then:
```py
from iantirta.text import romanize

romanize("你好")
```

Output:

```py
ni hao
```

## Japanese

Install Japanese support:

```bash
pip install "iantirta-text[ja]"
```

Then:

```py
from iantirta.text import romanize

romanize("日本語です")
```

Output:

```py
nihongo desu
```

## Mixed Text

Romanization can process mixed text:

```py
romanize("hello 你好 日本語です")
```

Output:

```py
hello ni hao nihongo desu
```

## Explicit Language

A language can be specified explicitly:

```py
romanize(
    "日本語",
    language="ja",
)
```

Supported languages currently include:
- `zh` — Chinese
- `ja` — Japanese

Language-specific dependencies are loaded only when required.
