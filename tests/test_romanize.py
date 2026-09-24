import pytest

from iantirta.text import romanize
from iantirta.text.romanize import _segment_text


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        # Empty / ordinary text
        ("", ""),
        ("hello", "hello"),
        ("Hello World", "Hello World"),
        ("hello world 123", "hello world 123"),

        # Chinese
        ("你好", "ni hao"),
        ("中国", "zhong guo"),
        ("你好世界", "ni hao shi jie"),

        # Japanese
        ("こんにちは", "konnichiha"),
        ("ありがとう", "arigatou"),

        # Mixed text
        ("hello 你好", "hello ni hao"),
        ("你好 hello", "ni hao hello"),
        ("hello こんにちは", "hello konnichiha"),

        # Mixed Chinese / Japanese
        ("你好 こんにちは", "ni hao konnichiha"),

        # Punctuation
        ("你好！", "ni hao！"),
        ("こんにちは！", "konnichiha！"),
    ],
)
def test_romanize_auto(text: str, expected: str) -> None:
    assert romanize(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("你好", "ni hao"),
        ("中国", "zhong guo"),
        ("你好世界", "ni hao shi jie"),
    ],
)
def test_romanize_chinese(text: str, expected: str) -> None:
    assert romanize(text, language="zh") == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("こんにちは", "konnichiha"),
        ("ありがとう", "arigatou"),
        ("日本語", "nihongo"),
    ],
)
def test_romanize_japanese(text: str, expected: str) -> None:
    assert romanize(text, language="ja") == expected


@pytest.mark.parametrize(
    "language",
    [
        "en",
        "fr",
        "ko",
        "invalid",
    ],
)
def test_romanize_rejects_unsupported_language(language: str) -> None:
    with pytest.raises(ValueError):
        romanize("hello", language=language)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "value",
    [
        None,
        123,
        1.5,
        [],
        {},
    ],
)
def test_romanize_requires_string(value) -> None:
    with pytest.raises(TypeError):
        romanize(value)


def test_romanize_preserves_latin_text() -> None:
    text = "Hello, world!"

    assert romanize(text) == text


def test_romanize_preserves_numbers() -> None:
    text = "Song 123 - hello"

    assert romanize(text) == text


def test_romanize_preserves_whitespace() -> None:
    text = "hello   你好   world"

    assert romanize(text) == "hello   ni hao   world"


def test_romanize_japanese_kanji_with_kana() -> None:
    assert romanize("日本語です") == "nihongodesu"


def test_romanize_han_only_is_ambiguous() -> None:
    # Automatic mode currently treats Han-only text as Chinese.
    assert romanize("日本") == "ri ben"


def test_romanize_han_can_be_forced_to_japanese() -> None:
    assert romanize("日本語", language="ja") == "nihongo"


def test_segment_text() -> None:
    assert _segment_text("hello 你好") == [
        ("hello ", None),
        ("你好", "zh"),
    ]


def test_segment_text_mixed_japanese() -> None:
    assert _segment_text("hello 日本語です") == [
        ("hello ", None),
        ("日本語です", "ja"),
    ]


def test_segment_text_han_defaults_to_chinese() -> None:
    assert _segment_text("hello 日本語") == [
        ("hello ", None),
        ("日本語", "zh"),
    ]
