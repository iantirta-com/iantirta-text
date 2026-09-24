# Part of Iantirta.com
# See LICENSE file for full copyright and licensing details.

from __future__ import annotations

import re
import typing as t
import unicodedata


Language = t.Literal["zh", "ja", "ko"]


__all__ = [
    "Language",
    "romanize",
]


_RE_HIRAGANA = re.compile(r"[\u3040-\u309f]")
_RE_KATAKANA = re.compile(r"[\u30a0-\u30ff]")
_RE_HAN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uF900-\uFAFF]")


def _is_hiragana(char: str) -> bool:
    return bool(_RE_HIRAGANA.fullmatch(char))


def _is_katakana(char: str) -> bool:
    return bool(_RE_KATAKANA.fullmatch(char))


def _is_han(char: str) -> bool:
    return bool(_RE_HAN.fullmatch(char))


def _is_japanese(char: str) -> bool:
    return _is_hiragana(char) or _is_katakana(char)


def _is_latin(char: str) -> bool:
    """
    Return whether a character belongs to the Latin script.

    Unicode does not provide a direct ``script`` property through the
    standard library, so we use the character name.
    """
    try:
        return "LATIN" in unicodedata.name(char)
    except ValueError:
        return False


def _detect_language(text: str) -> Language | None:
    """
    Infer the romanization language from a text segment.

    Japanese is detected when Hiragana or Katakana is present.
    Han-only text is treated as Chinese because Han characters alone
    cannot reliably distinguish Chinese from Japanese Kanji.

    This is intentionally script-based rather than statistical language
    detection.
    """
    if any(_is_japanese(char) for char in text):
        return "ja"

    if any(_is_han(char) for char in text):
        return "zh"

    return None


def _segment_text(text: str) -> list[tuple[str, Language | None]]:
    """
    Split text into chunks that can be processed independently.

    Latin text, punctuation, numbers, whitespace, etc. are preserved.
    Han/Kana portions are grouped together so that Japanese text such as
    ``日本語`` followed by Kana can be passed to pykakasi as one unit.
    """
    segments: list[tuple[str, Language | None]] = []

    current: list[str] = []
    current_kind: Language | None = None

    def flush() -> None:
        nonlocal current, current_kind

        if current:
            segments.append(("".join(current), current_kind))

        current = []
        current_kind = None

    for char in text:
        if _is_japanese(char):
            kind: Language = "ja"

            if current_kind in (None, "zh"):
                # If we have Han immediately before Kana, that entire
                # run should be Japanese.
                if current_kind == "zh":
                    current_kind = "ja"
                    current.append(char)
                    continue

        elif _is_han(char):
            # Han is ambiguous. We initially treat it as Japanese if the
            # surrounding segment is already Japanese.
            kind = "ja" if current_kind == "ja" else "zh"

        else:
            kind = None

        if kind != current_kind:
            flush()
            current_kind = kind

        current.append(char)

    flush()

    return segments


def _romanize_chinese(text: str) -> str:
    """
    Romanize Chinese text using Hanyu Pinyin.

    ``pypinyin`` is imported lazily so that it is not required merely to
    import ``iantirta.text``.
    """
    try:
        from pypinyin import Style, pinyin
    except ImportError as exc:
        raise ImportError(
            "Chinese romanization requires 'pypinyin'. "
            "Install it with: pip install 'iantirta-text[zh]'"
        ) from exc

    result = pinyin(
        text,
        style=Style.NORMAL,
        heteronym=False,
    )

    return " ".join(
        item[0]
        for item in result
        if item
    )


def _romanize_japanese(text: str) -> str:
    """
    Romanize Japanese text using Hepburn romanization.

    ``pykakasi`` is imported lazily so that it is not required merely to
    import ``iantirta.text``.
    """
    try:
        from pykakasi import kakasi
    except ImportError as exc:
        raise ImportError(
            "Japanese romanization requires 'pykakasi'. "
            "Install it with: pip install 'iantirta-text[ja]'"
        ) from exc

    converter = kakasi()

    result = converter.convert(text)

    return "".join(
        item["hepburn"]
        for item in result
        if item.get("hepburn")
    )


def romanize(
    text: str,
    *,
    language: Language | None = None,
) -> str:
    """
    Convert text into a Latin-script representation.

    Latin text is preserved. Characters written in other scripts
    are romanized when a supported romanization method is available.

    When ``language`` is not specified, the function attempts to
    determine the appropriate romanization method from the text.
    This allows mixed-script strings to be processed as a single
    input.

    Parameters
    ----------
    text:
        Text to romanize.

    language:
        Optional language code used to select a specific
        romanization method.

        Supported languages:

        ``"ja"``
            Japanese using hepburn.

        ``"zh"``
            Chinese using Hanyu.

        ``"ko"``
            Korean romanization.

        If ``None``, the language is inferred from the characters
        in the text where possible. Mixed-script text is processed
        according to the script of each portion.

    Returns
    -------
    str
        The romanized text.

    Raises
    ------
    ValueError
        If an unsupported language code is provided.

    Examples
    --------
    >>> romanize("hello")
    'hello'

    >>> romanize("こんにちは", language="ja")
    'konnichiha'

    >>> romanize("你好", language="zh")
    'ni hao'

    >>> romanize("hello 你好 こんにちは")
    'hello ni hao konnichiha'

    Notes
    -----
    Some scripts, particularly Han characters, are shared by
    multiple languages. Automatic detection cannot always
    determine the intended language from the characters alone.
    Specify ``language`` when the distinction matters.
    """
    if not isinstance(text, str):
        raise TypeError(
            f"text must be str, not {type(text).__name__}"
        )

    if not text:
        return ""

    if language not in (None, "zh", "ja"):
        raise ValueError(
            f"Unsupported language: {language!r}. "
            "Expected one of: 'zh', 'ja', or None."
        )

    # Explicit language:
    #
    # This is useful when the caller knows the language and removes
    # ambiguity from Han characters.
    if language == "zh":
        return _romanize_chinese(text)

    if language == "ja":
        return _romanize_japanese(text)

    # Automatic mode.
    segments = _segment_text(text)

    output: list[str] = []

    for segment, detected_language in segments:
        if detected_language == "zh":
            output.append(_romanize_chinese(segment))

        elif detected_language == "ja":
            output.append(_romanize_japanese(segment))

        else:
            output.append(segment)

    return "".join(output)
