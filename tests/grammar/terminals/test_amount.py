import typing

import pytest
from lark import Lark
from lark.exceptions import UnexpectedInput


@pytest.fixture
def amount_parser(make_parser: typing.Callable) -> Lark:
    return make_parser(module="beancount", rule="amount", ignore_spaces=True)


@pytest.fixture
def amount_tolerance_parser(make_parser: typing.Callable) -> Lark:
    return make_parser(module="beancount", rule="amount_tolerance", ignore_spaces=True)


_INVALID_AMOUNT_TOLERANCES = (
    '12.34 ~ USD',
    '~ 0.01 USD',
    '12.34 0.01 USD',
    '12.34 USD 0.01 USD',
    '12.34 USD ~ 0.01 USD',
    '(12.34 ~ 0.01) USD',
    '12.34 USD ~ 0.01',
    '12.34 USD ~ 0.01 USD',
)

@pytest.mark.parametrize(
    "text",
    [
        "12.34 USD",
        "-12.34 USD",
        "0.0 USD",
        "1+2 USD",
        "(1+2) USD",
        "500 BTC",
    ],
)
def test_parse_amount(amount_parser: Lark, text: str):
    amount_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    _INVALID_AMOUNT_TOLERANCES + (
        "12.34",
        "USD",
        "0..0 USD",
        "1+ USD",
        '12.34 ~ 0.01 USD',
    ),
)
def test_parse_bad_amount(amount_parser: Lark, text: str):
    with pytest.raises(UnexpectedInput):
        amount_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    [
        '12.34 ~ 0.01 USD',
    ],
)
def test_parse_amount_tolerance(amount_tolerance_parser: Lark, text: str):
    amount_tolerance_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    _INVALID_AMOUNT_TOLERANCES,
)
def test_parse_bad_amount_tolerance(amount_tolerance_parser: Lark, text: str):
    with pytest.raises(UnexpectedInput):
        amount_tolerance_parser.parse(text)
