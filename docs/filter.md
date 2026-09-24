# Filtering

The `filter_text()` function removes specified text fragments.

## Basic Usage

```python
from iantirta.text import filter_text

filter_text(
    "hello world",
    ["world"],
)
```

Result:

```py
hello
```

## Multiple Values

```py
filter_text(
    "hello world example",
    ["world", "example"],
)
```

## Whole-word Matching

Use `whole_word=True` to remove only complete word matches:

```py
filter_text(
    "hello helloworld",
    ["hello"],
    whole_word=True,
)
```

Result:

```py
 helloworld
```

The `hello` inside `helloworld` is not removed.

## Case Sensitivity

Matching is case-insensitive by default:

```py
filter_text(
    "Hello HELLO hello",
    ["hello"],
)
```

To make matching case-sensitive:

```py
filter_text(
    "Hello HELLO hello",
    ["hello"],
    case_sensitive=True,
)
```
