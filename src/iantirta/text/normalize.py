# Part of Iantirta.com
# See LICENSE file for full copyright and licensing details.

from __future__ import annotations

import re
import string
import typing as t
import unicodedata


UnicodeForm = t.Literal["NFC", "NFD", "NFKC", "NFKD"]

_PUNCTUATION_TRANSLATOR = str.maketrans("", "", string.punctuation)
_KALDI_PATTERN = re.compile(r"[<\[][^>\]]*[>\]]")


def normalize(
    text: str,
    *,
    unicode: UnicodeForm | t.Literal[False] = "NFKC",
    lowercase: bool = True,
    strip: bool = True,
    punctuation: bool = False,
    whitespace: bool = True,
    kaldi: bool = False,
) -> str:
    """
    Normalize text for comparison and text processing.

    Parameters
    ----------
    text:
        The text to normalize.

    unicode:
        Unicode normalization form to apply.

        Supported forms are ``"NFC"``, ``"NFD"``, ``"NFKC"``,
        and ``"NFKD"``. Set to ``False`` to disable Unicode
        normalization.

    lowercase:
        Convert alphabetic characters to lowercase.

    strip:
        Remove leading and trailing whitespace.

    punctuation:
        Remove ASCII punctuation characters.

    whitespace:
        Collapse consecutive whitespace characters into a single
        space.

    kaldi:
        Apply Kaldi-style text normalization. This removes
        bracketed annotations such as ``[noise]`` and ``<unk>``,
        removes punctuation, converts text to lowercase, and
        strips surrounding whitespace.

        Explicit normalization options are still applied after the
        Kaldi-specific processing.

    Returns
    -------
    str
        The normalized text.

    Examples
    --------
    >>> normalize("  Hello, WORLD!  ")
    'hello, world!'

    >>> normalize("  Hello, WORLD!  ", punctuation=True)
    'hello world'

    >>> normalize("  HELLO   WORLD  ")
    'hello world'

    >>> normalize("[noise] Hello, WORLD!", kaldi=True)
    'hello world'

    >>> normalize("ＡＢＣ", unicode="NFKC")
    'ABC'

    >>> normalize("ＡＢＣ", unicode=False)
    'ＡＢＣ'
    """
    if kaldi:
        text = _KALDI_PATTERN.sub("", text)
        punctuation = True
        lowercase = True
        strip = True

    if unicode:
        text = unicodedata.normalize(unicode, text)

    if punctuation:
        text = text.translate(_PUNCTUATION_TRANSLATOR)

    if lowercase:
        text = text.lower()

    if whitespace:
        text = " ".join(text.split())

    if strip:
        text = text.strip()

    return text
