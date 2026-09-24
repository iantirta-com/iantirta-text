import pytest

from iantirta.text import filter_text


@pytest.mark.parametrize(
    ("text", "remove", "expected"),
    [
        ("hello world", ["world"], "hello "),
        ("hello world", ["hello"], " world"),
        ("hello helloworld", ["hello"], " world"),
        ("hello world hello", ["hello"], " world "),
        ("abcabcabc", ["abc"], ""),
    ],
)
def test_filter_text(
    text: str,
    remove: list[str],
    expected: str,
) -> None:
    assert filter_text(text, remove) == expected


def test_filter_text_multiple_items() -> None:
    assert filter_text(
        "hello world test",
        ["hello", "test"],
    ) == " world "


def test_filter_text_multiple_items_overlapping() -> None:
    assert filter_text(
        "hello world",
        ["hello", "world"],
    ) == " "


def test_filter_text_case_insensitive() -> None:
    assert filter_text(
        "Hello HELLO hello",
        ["hello"],
    ) == "  "


def test_filter_text_case_sensitive() -> None:
    assert filter_text(
        "Hello HELLO hello",
        ["hello"],
        case_sensitive=True,
    ) == "Hello HELLO "


def test_filter_text_whole_word() -> None:
    assert filter_text(
        "hello helloworld",
        ["hello"],
        whole_word=True,
    ) == " helloworld"


def test_filter_text_whole_word_case_insensitive() -> None:
    assert filter_text(
        "Hello hello HELLO",
        ["hello"],
        whole_word=True,
    ) == "  "


def test_filter_text_whole_word_case_sensitive() -> None:
    assert filter_text(
        "Hello hello HELLO",
        ["hello"],
        whole_word=True,
        case_sensitive=True,
    ) == "Hello  HELLO"


def test_filter_text_whole_word_with_punctuation() -> None:
    assert filter_text(
        "hello, hello! (hello)",
        ["hello"],
        whole_word=True,
    ) == ", ! ()"


def test_filter_text_substring_matching() -> None:
    assert filter_text(
        "hello helloworld",
        ["hello"],
        whole_word=False,
    ) == " world"


def test_filter_text_empty_remove_item() -> None:
    assert filter_text(
        "hello world",
        ["", "world"],
    ) == "hello "


def test_filter_text_empty_remove_list() -> None:
    assert filter_text(
        "hello world",
        [],
    ) == "hello world"


def test_filter_text_remove_is_generator() -> None:
    remove = (item for item in ["hello", "world"])

    assert filter_text(
        "hello world",
        remove,
    ) == " "


def test_filter_text_escapes_regex_characters() -> None:
    assert filter_text(
        "hello.world hello*world",
        [".", "*"],
    ) == "helloworld helloworld"
