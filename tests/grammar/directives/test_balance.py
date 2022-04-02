import typing

import pytest
from lark import Lark
from lark.exceptions import UnexpectedInput


@pytest.fixture
def balance_parser(make_parser: typing.Callable) -> Lark:
    return make_parser(module="beancount", rule="balance", ignore_spaces=True)


@pytest.mark.parametrize(
    "text",
    [
        "2022-03-31 balance Assets 12.34 USD",
        "2022-03-31 balance Assets:Bank 45.67 BTC",
    ],
)
def test_parse_balance(balance_parser: Lark, text: str):
    balance_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    [
        "balance Assets",
        "2022-03-1 balance Assets:Bank",
        "2022-03 balance Assets:Bank USD",
        "2022-03-31 balance Assets:Bank 123",
    ],
)
def test_parse_bad_open(balance_parser: Lark, text: str):
    with pytest.raises(UnexpectedInput):
        balance_parser.parse(text)
