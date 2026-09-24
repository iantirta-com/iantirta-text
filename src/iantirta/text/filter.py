# Part of Iantirta.com
# See LICENSE file for full copyright and licensing details.

from __future__ import annotations

import re
import typing as t


def filter_text(
    text: str,
    remove: t.Iterable[str],
    *,
    whole_word: bool = False,
    case_sensitive: bool = False,
) -> str:
    """
    Remove specified text from a string.

    Parameters
    ----------
    text:
        Source text to filter.

    remove:
        Text fragments to remove.

    whole_word:
        If ``True``, only remove matches that form complete words.
        If ``False``, remove matching text wherever it occurs.

    case_sensitive:
        If ``True``, matching is case-sensitive. If ``False``,
        uppercase and lowercase forms are treated as equivalent.

    Returns
    -------
    str
        The filtered text.

    Examples
    --------
    >>> filter_text("hello world", ["world"])
    'hello '

    >>> filter_text("hello world", ["world"], whole_word=True)
    'hello '

    >>> filter_text("hello helloworld", ["hello"])
    '  world'

    >>> filter_text("hello helloworld", ["hello"], whole_word=True)
    'hello helloworld'

    >>> filter_text("Hello HELLO hello", ["hello"])
    '  '

    >>> filter_text("Hello HELLO hello", ["hello"], case_sensitive=True)
    'Hello HELLO '
    """
    for item in remove:
        if not item:
            continue

        if whole_word:
            pattern = rf"\b{re.escape(item)}\b"
        else:
            pattern = re.escape(item)

        flags = 0 if case_sensitive else re.IGNORECASE
        text = re.sub(pattern, "", text, flags=flags)

    return text
