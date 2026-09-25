import pytest

from iantirta.text import Alignment, align, distance, similarity


def test_distance_equal() -> None:
    assert distance("hello", "hello") == 0


def test_distance_insertion() -> None:
    assert distance("hello", "helloo") == 1


def test_distance_deletion() -> None:
    assert distance("helloo", "hello") == 1


def test_distance_substitution() -> None:
    assert distance("hello", "hallo") == 1


def test_distance_classic_example() -> None:
    assert distance("kitten", "sitting") == 3


def test_distance_empty_left() -> None:
    assert distance("", "hello") == 5


def test_distance_empty_right() -> None:
    assert distance("hello", "") == 5


def test_distance_generic_sequence() -> None:
    assert distance(
        ["hello", "world"],
        ["hello", "there"],
    ) == 1


# Aligmnet

def test_align_equal() -> None:
    assert align("abc", "abc") == [
        Alignment("equal", "a", "a"),
        Alignment("equal", "b", "b"),
        Alignment("equal", "c", "c"),
    ]


def test_align_replace() -> None:
    assert align("abc", "axc") == [
        Alignment("equal", "a", "a"),
        Alignment("replace", "b", "x"),
        Alignment("equal", "c", "c"),
    ]


def test_align_insert() -> None:
    assert align("abc", "abxc") == [
        Alignment("equal", "a", "a"),
        Alignment("equal", "b", "b"),
        Alignment("insert", None, "x"),
        Alignment("equal", "c", "c"),
    ]


def test_align_delete() -> None:
    assert align("abxc", "abc") == [
        Alignment("equal", "a", "a"),
        Alignment("equal", "b", "b"),
        Alignment("delete", "x", None),
        Alignment("equal", "c", "c"),
    ]


def test_align_distance_matches() -> None:
    result = align("kitten", "sitting")

    edits = sum(
        operation.operation != "equal"
        for operation in result
    )

    assert edits == distance("kitten", "sitting")


def test_similarity_equal() -> None:
    assert similarity("hello", "hello") == 1.0


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        ("hello", "hello", 1.0),
        ("HELLO", "HELLO", 1.0),
    ],
)
def test_similarity_identical(left, right, expected):
    assert similarity(left, right) == pytest.approx(expected)


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        ("hello", "HELLO", 0.0),
        ("HeLLO", "heLLo", 0.6),
        ("oh-eh", "oheh", 0.8),
    ],
)
def test_similarity_case_and_punctuation(
    left: str,
    right: str,
    expected: float,
) -> None:
    assert similarity(left, right) == pytest.approx(expected)


def test_similarity_substitution() -> None:
    assert similarity("hello", "hallo") == 0.8


def test_similarity_different() -> None:
    assert similarity("hello", "world") == pytest.approx(0.2)


def test_similarity_insertion() -> None:
    assert similarity("hello", "helloo") == 5 / 6


def test_similarity_empty() -> None:
    assert similarity("", "") == 1.0
    assert similarity("", "hello") == 0.0


def test_similarity_generic_sequence() -> None:
    assert similarity(
        ["hello", "world"],
        ["hello", "there"],
    ) == 0.5


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        ("HeLLO", "heLLo", 1.0),
        ("hello", "HELLO", 1.0),
        ("HeLLO", "heLLo", 1.0),
        ("oh-eh", "oheh", 1.0),
        (" hello", "hello ", 1.0),
        ("你好", "ni hao", 0.0),
        (
            ["hello", "world"],
            ["hello", "there"],
            0.5,
        ),
    ],
)
def test_similarity_normalized_text(
    left: str,
    right: str,
    expected: float,
) -> None:
    assert similarity(
        left, right,
        normalize={
            "punctuation": True
        }
    ) == pytest.approx(expected)
