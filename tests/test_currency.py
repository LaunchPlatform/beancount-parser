import typing

import pytest
from lark import Lark
from lark.exceptions import UnexpectedCharacters


@pytest.fixture
def currency_parser(make_parser: typing.Callable) -> Lark:
    return make_parser(module="currency", rule="CURRENCY", ignore_spaces=True)


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
