import typing

import pytest
from lark import Lark
from lark.exceptions import UnexpectedInput


@pytest.fixture
def amount_parser(make_parser: typing.Callable) -> Lark:
    return make_parser(module="amount", rule="AMOUNT", ignore_spaces=True)


@pytest.mark.parametrize(
    "text",
    [
        "12.34 USD",
        "-12.34 USD",
        "0.0 USD",
        "500 BTC",
    ],
)
def test_parse_amount(amount_parser: Lark, text: str):
    amount_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    [
        "12.34",
        "USD",
        "0..0 USD",
    ],
)
def test_parse_bad_amount(amount_parser: Lark, text: str):
    with pytest.raises(UnexpectedInput):
        amount_parser.parse(text)
