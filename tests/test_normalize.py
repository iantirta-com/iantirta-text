import pytest

from iantirta.text import normalize


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("", ""),
        ("hello", "hello"),
        ("Hello World", "hello world"),
        ("  Hello World  ", "hello world"),
        ("  HELLO   WORLD  ", "hello world"),
        ("hello\tworld\nagain", "hello world again"),
    ],
)
def test_normalize_default(text: str, expected: str) -> None:
    assert normalize(text) == expected


def test_normalize_unicode_nfkc() -> None:
    assert normalize("ＡＢＣ", unicode="NFKC") == "abc"


def test_normalize_unicode_nfc() -> None:
    text = "e\u0301"
    assert normalize(text, unicode="NFC") == "é"


def test_normalize_unicode_disabled() -> None:
    assert normalize("ＡＢＣ", unicode=False) == "ａｂｃ"


def test_normalize_unicode_disabled() -> None:
    assert normalize(
        "ＡＢＣ",
        unicode=False,
        lowercase=False,
    ) == "ＡＢＣ"


def test_normalize_lowercase_disabled() -> None:
    assert normalize("Hello WORLD", lowercase=False) == "Hello WORLD"


def test_normalize_strip_disabled() -> None:
    assert normalize("  hello  ", strip=False) == "hello"


def test_normalize_whitespace_disabled() -> None:
    assert normalize("hello   world", whitespace=False) == "hello   world"


def test_normalize_punctuation() -> None:
    assert normalize("Hello, WORLD!", punctuation=True) == "hello world"


def test_normalize_punctuation_disabled() -> None:
    assert normalize("Hello, WORLD!") == "hello, world!"


def test_normalize_ascii_punctuation() -> None:
    assert normalize(
        "hello! @world #test$",
        punctuation=True,
    ) == "hello world test"


def test_normalize_kaldi() -> None:
    assert normalize("[noise] Hello, WORLD!", kaldi=True) == "hello world"


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("[noise] hello", "hello"),
        ("<unk> hello", "hello"),
        ("[noise] <unk> hello", "hello"),
        ("hello [noise] world", "hello world"),
        ("hello <unk> world", "hello world"),
    ],
)
def test_normalize_kaldi_removes_annotations(
    text: str,
    expected: str,
) -> None:
    assert normalize(text, kaldi=True) == expected


def test_normalize_kaldi_overrides_options() -> None:
    assert normalize(
        "[noise] Hello, WORLD!",
        kaldi=True,
        lowercase=False,
        punctuation=False,
        strip=False,
    ) == "hello world"


def test_normalize_combined_options() -> None:
    assert normalize(
        "  ＨＥＬＬＯ,   WORLD!  ",
        unicode="NFKC",
        lowercase=True,
        strip=True,
        punctuation=True,
        whitespace=True,
    ) == "hello world"


def test_normalize_unicode_nfkd() -> None:
    assert normalize("é", unicode="NFKD") == "e\u0301"


def test_normalize_unicode_nfd() -> None:
    assert normalize("é", unicode="NFD") == "e\u0301"


@pytest.mark.parametrize(
    ("form", "text", "expected"),
    [
        ("NFC", "e\u0301", "é"),
        ("NFD", "é", "e\u0301"),
        ("NFKC", "Ａ", "A"),
        ("NFKD", "Ａ", "A"),
    ],
)
def test_normalize_unicode_forms(
    form: str,
    text: str,
    expected: str,
) -> None:
    assert normalize(
        text,
        unicode=form,
        lowercase=False,
    ) == expected
