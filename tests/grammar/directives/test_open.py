import typing

import pytest
from lark import Lark
from lark.exceptions import UnexpectedInput


@pytest.fixture
def open_parser(make_parser: typing.Callable) -> Lark:
    return make_parser(module="beancount", rule="open", ignore_spaces=True)


@pytest.mark.parametrize(
    "text",
    [
        "2022-03-31 open Assets:Bank",
        "2022-03-31 open Assets:Bank USD",
        "2022-03-31 open Assets:Bank USD,BTC",
        '2022-03-31 open Assets:Bank USD,BTC "STRICT"',
        '2022-03-31 open Assets:Bank "STRICT"',
        '2022-03-31 open Assets:Bank USD,BTC "NONE"',
        '2022-03-1 open Assets:Bank',
    ],
)
def test_parse_open(open_parser: Lark, text: str):
    open_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    [
        "open Assets:Bank",
        "2022-03 open Assets:Bank USD",
        "2022-03-31 open Assets",
        "2022-03-31 open Assets:Bank 123",
        '2022-03-31 open USD,BTC "STRICT"',
        '2022-03-31 open assets:bank USD,BTC "NONE"',
    ],
)
def test_parse_bad_open(open_parser: Lark, text: str):
    with pytest.raises(UnexpectedInput):
        open_parser.parse(text)
