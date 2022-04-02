import typing

import pytest
from lark import Lark
from lark.exceptions import UnexpectedInput


@pytest.fixture
def transaction_parser(make_parser: typing.Callable) -> Lark:
    return make_parser(module="beancount", rule="txn", ignore_spaces=True)


@pytest.mark.parametrize(
    "text",
    [
        "1970-01-01",
        '1970-01-01 * "Foobar"',
        '1970-01-01 ! "Foobar"',
        '1970-01-01 ! "\\"Foobar\\""',
        '1970-01-01 ! "Jane Doe" "Foobar"',
        '1970-01-01 ! "Jane Doe" "Foobar" #hash-tag',
        '1970-01-01 ! "Jane Doe" "Foobar" #hash-tag ^link',
        '1970-01-01 ! "Jane Doe" "Foobar" #hash-tag ^link-1 #hash2',
        '1970-01-01 txn "Jane Doe" "Foobar"',
    ],
)
def test_parse_transaction(transaction_parser: Lark, text: str):
    transaction_parser.parse(text)


@pytest.mark.parametrize(
    "text",
    [
        '1970-01-01 @ "Foobar"',
        "1970-01-01 ! Foobar",
        '1970-01-01 ! "Jane Doe" Foobar',
        '1970-01-01 TXN "Jane Doe" "Foobar"',
        'TXN "Jane Doe" "Foobar"',
    ],
)
def test_parse_bad_transaction(transaction_parser: Lark, text: str):
    with pytest.raises(UnexpectedInput):
        transaction_parser.parse(text)
