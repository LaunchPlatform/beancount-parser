import pytest
from lark import Lark
from lark.exceptions import UnexpectedCharacters

from beancount_parser.parser import GRAMMAR_FOLDER


@pytest.fixture
def number_parser() -> Lark:
    return Lark(
        """
    start: NUMBER
    %import .numbers.NUMBER
    """,
        import_paths=[GRAMMAR_FOLDER],
    )


@pytest.fixture
def signed_number_parser() -> Lark:
    return Lark(
        """
    start: SIGNED_NUMBER
    %import .numbers.SIGNED_NUMBER
    """,
        import_paths=[GRAMMAR_FOLDER],
    )


@pytest.mark.parametrize(
    "text",
    [
        "0",
        "1234",
        "4578",
        "12.34",
        ".34",
        "0.0",
    ],
)
def test_parse_number(number_parser: Lark, text: str):
    number_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    [
        "-0",
        "+1234",
        "-5.67",
        "4578.123.45",
        "0x12.34",
        "..34",
        "0.0.",
        "abc",
    ],
)
def test_parse_bad_number(number_parser: Lark, text: str):
    with pytest.raises(UnexpectedCharacters):
        number_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    [
        "0",
        "1234",
        "4578",
        "12.34",
        "12.34",
        ".34",
        "0.0",
        "-5",
        "-5.67",
        "+5.67",
    ],
)
def test_parse_signed_number(signed_number_parser: Lark, text: str):
    signed_number_parser.parse(text)


@pytest.mark.parametrize("text", ["0a", "1234..", "..4578", "12..34", "abc"])
def test_parse_bad_signed_number(signed_number_parser: Lark, text: str):
    with pytest.raises(UnexpectedCharacters):
        signed_number_parser.parse(text)
