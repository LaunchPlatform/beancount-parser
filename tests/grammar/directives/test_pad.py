import typing

import pytest
from lark import Lark
from lark.exceptions import UnexpectedInput


@pytest.fixture
def pad_parser(make_parser: typing.Callable) -> Lark:
    return make_parser(module="beancount", rule="pad", ignore_spaces=True)


@pytest.mark.parametrize(
    "text",
    [
        "2022-03-31 pad Assets Expenses",
    ],
)
def test_parse_pad(pad_parser: Lark, text: str):
    pad_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    [
        "pad Assets",
        "2022-03-1 pad Assets:Bank",
        "2022-03 pad Assets:Bank USD",
        "2022-03-31 pad Assets:Bank 123",
        '2022-03-31 pad USD,BTC "STRICT"',
        '2022-03-31 pad Foobar USD,BTC "NONE"',
    ],
)
def test_parse_bad_pad(pad_parser: Lark, text: str):
    with pytest.raises(UnexpectedInput):
        pad_parser.parse(text)
