# Normalization

The `normalize()` function provides configurable Unicode and text
normalization.

## Basic Usage

```python
from iantirta.text import normalize

normalize("  Hello World  ")
```

By default, text is:

- Unicode-normalized using NFKC
- converted to lowercase
- stripped of leading and trailing whitespace
- normalized for repeated whitespace


## Unicode Normalization

Choose a Unicode normalization form:

```py
normalize(
    "ＡＢＣ",
    unicode="NFKC",
    lowercase=False,
)
```

Supported forms are:

- `NFC`
- `NFD`
- `NFKC`
- `NFKD`

Unicode normalization can be disabled:

```py
normalize(
    "ＡＢＣ",
    unicode=False,
)
```

## Lowercase

Disable lowercasing with:

```py
normalize(
    "Hello World",
    lowercase=False,
)
```

## Punctuation

Punctuation is preserved by default.

To remove ASCII punctuation:

```py
normalize(
    "hello, world!",
    punctuation=True,
)
```

## Kaldi-style Cleanup

For text containing Kaldi-style markup:

```py
normalize(
    "<noise> hello [music]",
    kaldi=True,
)
```
