import pytest
from lark import Lark
from lark.exceptions import UnexpectedCharacters

from beancount_parser.parser import GRAMMAR_FOLDER


@pytest.fixture
def currency_parser() -> Lark:
    return Lark(
        """
    start: CURRENCY
    %import .currency.CURRENCY
    """,
        import_paths=[GRAMMAR_FOLDER],
    )


@pytest.mark.parametrize(
    "text",
    [
        "A",
        "AB",
        "USD",
        "ABC",
        "A.B",
        "A_B",
        "A-B",
        "A-B-C",
        "CONTRACT_HOURS",
    ],
)
def test_parse_currency(currency_parser: Lark, text: str):
    currency_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    [
        "a",
        "AbC",
        "ABc",
        "A12C",
        "@",
        "A@B",
    ],
)
def test_parse_bad_currency(currency_parser: Lark, text: str):
    with pytest.raises(UnexpectedCharacters):
        currency_parser.parse(text)
