# Part of Iantirta.com
# See LICENSE file for full copyright and licensing details.

from __future__ import annotations

import typing as t
from dataclasses import dataclass


__all__ = [
    "Alignment",
    "align",
    "distance",
]


T = t.TypeVar("T")


def distance(
    left: t.Sequence[T],
    right: t.Sequence[T],
) -> int:
    """
    Calculate the Levenshtein edit distance between two sequences.

    The distance is the minimum number of single-element operations
    required to transform ``left`` into ``right``.

    The supported operations are:

    - insertion
    - deletion
    - substitution

    Parameters
    ----------
    left:
        First sequence to compare.

    right:
        Second sequence to compare.

    Returns
    -------
    int
        Minimum number of insertions, deletions, and substitutions
        required to transform ``left`` into ``right``.

    Examples
    --------
    >>> distance("kitten", "sitting")
    3

    >>> distance("hello", "hello")
    0

    >>> distance("", "hello")
    5

    >>> distance(["a", "b", "c"], ["a", "x", "c"])
    1
    """
    if left == right:
        return 0

    if not left:
        return len(right)

    if not right:
        return len(left)

    # Keep the second sequence as the shorter dimension to reduce
    # memory usage.
    if len(left) < len(right):
        left, right = right, left

    previous = list(range(len(right) + 1))

    for left_item_index, left_item in enumerate(left, start=1):
        current = [left_item_index]

        for right_item_index, right_item in enumerate(right, start=1):
            insertion = current[right_item_index - 1] + 1
            deletion = previous[right_item_index] + 1
            substitution = previous[right_item_index - 1] + (
                left_item != right_item
            )

            current.append(
                min(
                    insertion,
                    deletion,
                    substitution,
                )
            )

        previous = current

    return previous[-1]


@dataclass(frozen=True, slots=True)
class Alignment(t.Generic[T]):
    """
    Represent a single alignment operation.

    Parameters
    ----------
    operation:
        Type of edit operation. One of ``"equal"``, ``"replace"``,
        ``"insert"``, or ``"delete"``.

    left:
        Element from the left sequence, or ``None`` when the operation
        does not contain a left-side element.

    right:
        Element from the right sequence, or ``None`` when the operation
        does not contain a right-side element.
    """

    operation: t.Literal["equal", "replace", "insert", "delete"]
    left: T | None
    right: T | None


def align(
    left: t.Sequence[T],
    right: t.Sequence[T],
) -> list[Alignment[T]]:
    """
    Align two sequences using Levenshtein edit distance.

    The returned operations describe how to transform ``left`` into
    ``right`` using insertions, deletions, and substitutions.

    Parameters
    ----------
    left:
        First sequence to compare.

    right:
        Second sequence to compare.

    Returns
    -------
    list[Alignment[T]]
        Ordered list of alignment operations required to transform
        ``left`` into ``right``.

    Examples
    --------
    >>> align("abc", "abc")
    [
        Alignment("equal", "a", "a"),
        Alignment("equal", "b", "b"),
        Alignment("equal", "c", "c"),
    ]

    >>> align("abc", "axc")
    [
        Alignment("equal", "a", "a"),
        Alignment("replace", "b", "x"),
        Alignment("equal", "c", "c"),
    ]

    >>> align("abc", "abxc")
    [
        Alignment("equal", "a", "a"),
        Alignment("equal", "b", "b"),
        Alignment("insert", None, "x"),
        Alignment("equal", "c", "c"),
    ]
    """
    # Build the complete dynamic-programming matrix.
    rows = len(left) + 1
    columns = len(right) + 1

    matrix = [
        [0] * columns
        for _ in range(rows)
    ]

    for i in range(rows):
        matrix[i][0] = i

    for j in range(columns):
        matrix[0][j] = j

    for i in range(1, rows):
        for j in range(1, columns):
            substitution = matrix[i - 1][j - 1] + (
                left[i - 1] != right[j - 1]
            )

            insertion = matrix[i][j - 1] + 1
            deletion = matrix[i - 1][j] + 1

            matrix[i][j] = min(
                substitution,
                insertion,
                deletion,
            )

    # Backtrack from the bottom-right corner.
    operations: list[Alignment[T]] = []

    i = len(left)
    j = len(right)

    while i > 0 or j > 0:
        # Equal
        if (
            i > 0
            and j > 0
            and left[i - 1] == right[j - 1]
            and matrix[i][j] == matrix[i - 1][j - 1]
        ):
            operations.append(
                Alignment(
                    "equal",
                    left[i - 1],
                    right[j - 1],
                )
            )
            i -= 1
            j -= 1
            continue

        # Replace
        if (
            i > 0
            and j > 0
            and matrix[i][j] == matrix[i - 1][j - 1] + 1
        ):
            operations.append(
                Alignment(
                    "replace",
                    left[i - 1],
                    right[j - 1],
                )
            )
            i -= 1
            j -= 1
            continue

        # Insert
        if (
            j > 0
            and matrix[i][j] == matrix[i][j - 1] + 1
        ):
            operations.append(
                Alignment(
                    "insert",
                    None,
                    right[j - 1],
                )
            )
            j -= 1
            continue

        # Delete
        if (
            i > 0
            and matrix[i][j] == matrix[i - 1][j] + 1
        ):
            operations.append(
                Alignment(
                    "delete",
                    left[i - 1],
                    None,
                )
            )
            i -= 1
            continue

        raise RuntimeError("Invalid alignment state.")

    operations.reverse()

    return operations


def similarity(
    left: t.Sequence[T],
    right: t.Sequence[T],
    *,
    normalize: bool | t.Mapping[str, t.Any] = False,
) -> float:
    """
    Calculate normalized Levenshtein similarity between two sequences.

    The similarity is calculated from the Levenshtein edit distance:
    
    ``1 - distance(left, right) / max(len(left), len(right))``
    
    A similarity of ``1.0`` means the sequences are identical.
    A similarity of ``0.0`` means the edit distance is equal to the
    length of the longer sequence.

    Parameters
    ----------
    left:
        First sequence to compare.

    right:
        Second sequence to compare.

    normalize:
        Whether to normalize text before comparison.

        ``False`` performs a raw sequence comparison.

        ``True`` normalizes both inputs using the default
        :func:`iantirta.text.normalize` settings.

        A mapping is passed as keyword arguments to
        :func:`iantirta.text.normalize`.

    Returns
    -------
    float
        Similarity between ``0.0`` and ``1.0``.

    Examples
    --------
    >>> similarity("hello", "hello")
    1.0

    >>> similarity("hello", "hallo")
    0.8

    >>> similarity("hello", "world")
    0.0

    >>> similarity("", "")
    1.0

    >>> similarity("", "hello")
    0.0
    """
    from .normalize import normalize as normalize_text
    
    if normalize:
        kwargs = {} if normalize is True else dict(normalize)
        
        if isinstance(left, str):
            left = normalize_text(left, **kwargs)
        else:
            left = type(left)(
                normalize_text(item, **kwargs)
                for item in left
            )
    
        if isinstance(right, str):
            right = normalize_text(right, **kwargs)
        else:
            right = type(right)(
                normalize_text(item, **kwargs)
                for item in right
            )
        
    if left == right:
        return 1.0

    longest = max(len(left), len(right))

    if longest == 0:
        return 1.0

    return 1.0 - distance(left, right) / longest
